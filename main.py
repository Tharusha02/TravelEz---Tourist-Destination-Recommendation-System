from flask import Flask, render_template, request, url_for, session, redirect, jsonify, send_file
from flask_mysqldb import MySQL
import MySQLdb
from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery
import re
import json



app = Flask(__name__)

# Configuration for MySQL database
app.secret_key = 'xyzsdfg'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'travelez'

mysql = MySQL(app)



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

        if user_data:
            user_email, first_name, last_name, phone, address_line1, address_line2, city, country = user_data
            return render_template('profileEdit.html', username=user_username, email=user_email, first_name=first_name, last_name=last_name,phone=phone, address_line1=address_line1, address_line2=address_line2, city=city, country=country)
        
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
            cursor.execute("UPDATE user SET firstName = %s, lastName = %s, phone = %s, AddressLine1 = %s, AddressLine2 = %s, city = %s, country = %s WHERE username = %s",
                           (first_name, last_name, phone_no, address_line1, address_line2, city, country, user_username))
            mysql.connection.commit()
            cursor.close()

            return redirect(url_for('profileEdit'))
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


# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
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
            return redirect(url_for('search'))
        else:
            message = 'PLEASE ENTER CORRECT EMAIL / PASSWORD !'
    return render_template('login.html', message=message)
    

# Route for display username in search page
@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'loggedin' in session:
        user_username = session['username']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT firstName, lastName FROM user WHERE username = %s", (user_username,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            user_first_name, user_last_name = user
            return render_template('search.html', user1=user_first_name, user2=user_last_name)
           
    return redirect(url_for('login'))


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
    return redirect(url_for('login'))

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