from flask import Flask, render_template, request, url_for, session, redirect, jsonify, send_file, make_response
from flask_mysqldb import MySQL
import MySQLdb
from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery
import re
import json
# import test  # Importing test.py
from appp import predict, getCity


app = Flask(__name__)

# Configuration for MySQL database
app.secret_key = 'xyzsdfg'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'travelez'

mysql = MySQL(app)

# Function to handle RDF querying
def process_rdf_data(city):
    # Load your RDF data from a file or URL
    g = Graph()
    g.parse("onto.rdf") 

    # Define the namespace
    ns = Namespace("http://example.com/LocationCity#")

    # Define the SPARQL query with the user-input city for restaurants
    query_restaurants = prepareQuery(f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX City: <http://example.com/LocationCity#>

        SELECT ?restaurant ?comment
        WHERE {{
            ?restaurant rdfs:subClassOf City:{city}Restaurants;
                        rdfs:comment ?comment.
        }}
    """)

    restaurant_count = 0
    restaurants = {}  # Dictionary to store unique restaurants and their comments

    # Execute the query and iterate over the results
    for row in g.query(query_restaurants):
        if restaurant_count >= 5:  # Check if the counter reaches 5
            break  # If so, break out of the loop
        restaurant_uri = row[0]  # Get the URI of the restaurant
        restaurant_name = restaurant_uri.split("#")[-1]  # Extract restaurant name and split by capitalization
        restaurant_name = ' '.join(re.findall('[A-Z][a-z]*', restaurant_name))  # Join words by capitalization
        comment = row[1]  # Get the comment

        # Remove "Address:" and "Grade:" from the comment
        comment = comment.replace("Address:", "").replace("Grade:", "").strip()

        # Check if the restaurant name already exists in the dictionary
        if restaurant_name in restaurants:
            # If it does, append the comment to its list of comments
            restaurants[restaurant_name].append(comment)
        else:
            # If it doesn't, create a new list with the comment
            restaurants[restaurant_name] = [comment]
            restaurant_count += 1  # Increment the count

    # Define the SPARQL query for travel agents
    query_travel_agents = prepareQuery(f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX City: <http://example.com/LocationCity#>

        SELECT ?agent ?comment
        WHERE {{
            ?agent rdfs:subClassOf City:{city}TravelAgents;
                        rdfs:comment ?comment.
        }}
    """)

    agent_count = 0
    travel_agents = {}

    # Execute the query and iterate over the results
    for row in g.query(query_travel_agents):
        if agent_count >= 5:  # Check if the counter reaches 5
            break  # If so, break out of the loop
        agent_uri = row[0]  # Get the URI of the travel agent
        agent_name = agent_uri.split("#")[-1]  # Extract travel agent name and split by capitalization
        agent_name = ' '.join(re.findall('[A-Z][a-z]*', agent_name))  # Join words by capitalization
        comment = row[1]  # Get the comment

        # Remove any unwanted prefixes from the comment
        comment = comment.replace("Address:", "").strip()

        # Check if the travel agent name already exists in the dictionary
        if agent_name in travel_agents:
            # If it does, append the comment to its list of comments
            travel_agents[agent_name].append(comment)
        else:
            # If it doesn't, create a new list with the comment
            travel_agents[agent_name] = [comment]
            agent_count += 1  # Increment the count

    # Define the SPARQL query for accommodations
    query_accommodations = prepareQuery(f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX City: <http://example.com/LocationCity#>

        SELECT ?accommodation ?comment
        WHERE {{
            ?accommodation rdfs:subClassOf City:{city}Accommodation;
                           rdfs:comment ?comment.
        }}
    """)

    accommodation_count = 0
    accommodations = {}  # Dictionary to store unique accommodations and their comments

    # Execute the query and iterate over the results
    for row in g.query(query_accommodations):
        if accommodation_count >= 5:  # Check if the counter reaches 5
            break  # If so, break out of the loop
        accommodation_uri = row[0]  # Get the URI of the accommodation
        accommodation_name = accommodation_uri.split("#")[-1]  # Extract accommodation name and split by capitalization
        accommodation_name = ' '.join(re.findall('[A-Z][a-z]*', accommodation_name))  # Join words by capitalization
        comment = row[1]  # Get the comment

        # Remove "Type:" and "Address:" from the comment
        comment = comment.replace("Type:", "").replace("Address:", "").strip()

        # Check if the accommodation name already exists in the dictionary
        if accommodation_name in accommodations:
            # If it does, append the comment to its list of comments
            accommodations[accommodation_name].append(comment)
        else:
            # If it doesn't, create a new list with the comment
            accommodations[accommodation_name] = [comment]
            accommodation_count += 1  # Increment the count

    # Convert data to desired format

    # Convert restaurants, travel_agents, and accommodations to the desired format
    restaurants_list = [[name] + comments for name, comments in restaurants.items()]
    agents_list = [[name] + comments for name, comments in travel_agents.items()]
    accommodations_list = [[name] + comments for name, comments in accommodations.items()]

    output_data = {
        "restaurants": restaurants_list,
        "travel_agents": agents_list,
        "accommodations": accommodations_list
    }

    # Save the data to a text file in JSON format
    with open('output_data.txt', 'w') as file:
        json.dump(output_data, file)

    return output_data


# Route for the main page
@app.route('/')
def mainPage():
    return render_template('MainPage.html')

# Route for the signup form
@app.route('/signup')
def signup_form():
    return render_template('signup.html')

# Route for the login form
@app.route('/login')
def login_form():
    return render_template('login.html')

# Route for editing user profile
@app.route('/profileEdit')
def profileEdit():
    if 'loggedin' in session:
        user_username = session['username']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT email, firstName, lastName, phone, AddressLine1, AddressLine2, city, country FROM user WHERE username = %s", (user_username,))
        user_data = cursor.fetchone()
        cursor.close()

        message = session.pop('message', '')  # Get the message from the session and remove it
        
        if user_data:
            user_email, first_name, last_name, phone, address_line1, address_line2, city, country = user_data
            return render_template('profileEdit.html', username=user_username, email=user_email, first_name=first_name, last_name=last_name, phone=phone, address_line1=address_line1, address_line2=address_line2, city=city, country=country, message=message)
        
    return redirect(url_for('login'))

    
# Route for updating user profile
@app.route('/profileEdit', methods=['POST'])
def update_profile():
    if 'loggedin' in session:
        if request.method == 'POST':
            user_username = session['username']
            first_name = request.form['firstName']
            last_name = request.form['lastName']
            phone_no = request.form['phone']
            address_line1 = request.form['AddressLine1']
            address_line2 = request.form['AddressLine2']
            city = request.form['city']
            country = request.form['country']

            cursor = mysql.connection.cursor()
            try:
                cursor.execute("UPDATE user SET firstName = %s, lastName = %s, phone = %s, AddressLine1 = %s, AddressLine2 = %s, city = %s, country = %s WHERE username = %s",
                               (first_name, last_name, phone_no, address_line1, address_line2, city, country, user_username))
                mysql.connection.commit()
                cursor.close()
                session['message'] = "Profile updated successfully."  # Set the message in the session
            except Exception as e:
                mysql.connection.rollback()
                session['message'] = f"Error updating profile: {str(e)}"  # Set the error message in the session
                cursor.close()

            return redirect(url_for('profileEdit'))  # Redirect to profileEdit route to display the message
    return redirect(url_for('login'))


# Function to get destinations from the database
def get_destinations():

    # Create a cursor object
    cursor = mysql.connection.cursor()

    # Fetch destinations from the database
    cursor.execute("SELECT destination_name FROM destinations")
    destinations = cursor.fetchall()

    # Close cursor 
    cursor.close()

    # Return destinations
    return destinations


# Route for display username in review page 
@app.route('/review')
def review():
    if 'loggedin' in session:
        user_username = session['username']

        # Get destinations from the database
        destinations = get_destinations()
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT firstName, lastName FROM user WHERE username = %s", (user_username,))
        user = cursor.fetchone()

        # Fetch first 3 reviews from the database
        cursor.execute("SELECT username, destination, review FROM profile_review ORDER BY review_id DESC LIMIT 3")
        reviews = cursor.fetchall()

        cursor.close()

        if user:
            user_first_name = user[0]
            user_last_name = user[1]
            return render_template('review.html', user1=user_first_name, user2=user_last_name, destinations=destinations, reviews=reviews)
        
    return redirect(url_for('login'))


# Route for submitting review (POST method)
@app.route('/review', methods=['POST'])
def submitReview():
    if request.method == 'POST':
        if 'loggedin' in session:
            user_username = session['username']
            review_text = request.form['opinion']
            destination = request.form['destination']
            
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO profile_review (username, destination, review) VALUES (%s, %s, %s)", (user_username, destination, review_text))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('review'))  
        else:
            return render_template('login.html') 
    else:
        return render_template('review.html')
    

# Route for display username in review page 
@app.route('/aboutUs')
def aboutUs():
    if 'loggedin' in session:
        user_username = session['username']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT firstName, lastName FROM user WHERE username = %s", (user_username,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            user_first_name = user[0]
            user_last_name = user[1]
            return render_template('aboutUs.html', user1=user_first_name, user2=user_last_name)
        
    return redirect(url_for('login'))
    
from flask import request, session, redirect, url_for, render_template, make_response


# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session:
        return redirect(url_for('search'))  # Redirect if user is already logged in

    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['username'] = user['username']
            session['email'] = user['email']

            # Save login details in cookies
            resp = make_response(redirect(url_for('search')))
            resp.set_cookie('email', email)
            resp.set_cookie('password', password)
            return resp
        else:
            message = 'PLEASE ENTER CORRECT EMAIL / PASSWORD !'

    return render_template('login.html', message=message)


# Route for the display the destination
@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'loggedin' in session:
        user_username = session['username']
        user_preference = request.form.get('preference')

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT firstName, lastName FROM user WHERE username = %s", (user_username,))
        user = cursor.fetchone()
        cursor.close()

        if request.method == 'POST':  # Check if the form was submitted
            if user_preference:  # Check if preference is provided
                print("User preference:", user_preference)

                predicted_destination = predict(user_preference)
                print(predicted_destination)

                predicted_city = getCity(predicted_destination)
                print(predicted_city)

                rdf_data = process_rdf_data(predicted_city)
                print(rdf_data)

                if user:
                    user_first_name, user_last_name = user
                    return render_template('search.html', user1=user_first_name, user2=user_last_name, location=predicted_destination, rdf_data=rdf_data)
            else:
                # Display error message if preference is not provided
                error_message = "Please provide a preference."
                if user:
                    user_first_name, user_last_name = user
                    return render_template('search.html', error_message=error_message, user1=user_first_name, user2=user_last_name)
        
        # If the request method is not POST or preference is not provided, render the search page without error message
        if user:
            user_first_name, user_last_name = user
            return render_template('search.html', user1=user_first_name, user2=user_last_name)
        
    return redirect(url_for('login'))



@app.route('/output_data')
def get_output_data():
    return send_file('output_data.txt')  # Serve the output_data.txt file

# Route for user profile
@app.route('/profile')
def profilePage():
    if 'loggedin' in session:
        user_username = session['username']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT firstName, lastName FROM user WHERE username = %s", (user_username,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            user_first_name = user[0]
            user_last_name = user[1]
            return render_template('profile.html', username=user_username, user1=user_first_name, user2=user_last_name)
    
    return redirect(url_for('login'))

# Route for user logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('mainPage'))

# Route for user signup
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        username = request.form['Username']
        email = request.form['email']
        phone = request.form['phone']
        address_line1 = request.form['AddressLine1']
        address_line2 = request.form['AddressLine2']
        city = request.form['city']
        country = request.form['country']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        # Check if all fields are filled
        if not (first_name and last_name and username and email and phone and address_line1 and city and country and password and confirm_password):
            message = 'PLEASE FILL IN ALL FIELDS !'
            return render_template('signup.html', message=message)

        # Email validation
        if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
            message = 'INVALID EMAIL ADDRESS !'
            return render_template('signup.html', message=message)

        # Check if password and confirm password match
        if password != confirm_password:
            message = 'PASSWORD DO NOT MATCH'
            return render_template('signup.html', message=message)

        # Check if the username already exists
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            message = 'USERNAME ALREADY EXISTS. PLEASE CHOOSE A DIFFERENT ONE !'
            return render_template('signup.html', message=message)
        
        # If everything is fine, insert the new user into the database
        cursor.execute('''INSERT INTO user (firstName, lastName, username, email, phone, AddressLine1, AddressLine2, city, country, password, confirmPassword) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                  (first_name, last_name, username, email, phone, address_line1, address_line2, city, country, password, confirm_password))
        mysql.connection.commit()
        cursor.close()
        return render_template('login.html')
    

if __name__ == "__main__":
    
    app.run(debug=True)