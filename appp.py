

import pandas as pd
from flask import Flask, request, render_template
import pickle

#app = Flask(__name__)

# Load the model
loaded_model = pickle.load(open('destination_pred.pkl', 'rb'))
loaded_tfidf_vectorizer = pickle.load(open('tfidf_vectorizer.pkl', 'rb'))
loaded_id_to_category = pickle.load(open('id_to_category.pkl', 'rb'))

def preprocess_input(text):
    """
    Apply preprocessing to user input
    """
    cleaned_text = text.lower()
    return cleaned_text

#@app.route('/')
def home():
    return render_template('index.html')



#To use the predict button in our web-app
#@app.route('/predict',methods=['POST'])
def predict(user_input):
    #For rendering results on HTML GUI
    #user_input = request.form['pref']

    preprocessed_input = preprocess_input(user_input)
    user_vectorized = loaded_tfidf_vectorizer.transform([preprocessed_input])
    predicted_label_index = loaded_model.predict(user_vectorized)[0]
    predicted_location_name = loaded_id_to_category[predicted_label_index]

    #Capitalizing each word of the destination
    predicted_location_name = predicted_location_name.title()

    print(predicted_location_name)

    return predicted_location_name


   # return render_template('search.html', prediction_text='Location is  :{}'.format(predicted_location_name))
    # return render_template('search.html', location=predicted_location_name)


def getCity(user_input):
    dataset = pd.read_csv('Reviews.csv', encoding='ISO-8859-1')

    preprocessed_input = preprocess_input(user_input)
    user_vectorized = loaded_tfidf_vectorizer.transform([preprocessed_input])
    predicted_label_index = loaded_model.predict(user_vectorized)[0]
    location = loaded_id_to_category[predicted_label_index]
    location_name = location.title()

    city_name = dataset.loc[dataset['Location_Name'] == location_name, 'Located_City'].iloc[0]

    return city_name


#if __name__ == '__main__':
    #app.run(debug=True)
