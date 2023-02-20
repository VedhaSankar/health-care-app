from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime


load_dotenv()

PORT = os.environ.get('PORT')
MONGO_URI = os.environ.get('MONGO_URI')

client = MongoClient(MONGO_URI)  

DB_NAME = 'trials'
database = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def start():

    return render_template('index.html')


@app.route('/patient-registration', methods = ["GET", "POST"])
def patient_registration():

    if (request.method == "POST"):

        # get user input from html form

        first_name          = request.values.get("first_name")
        last_name           = request.values.get("last_name")
        email               = request.values.get("email")
        phone_number        = request.values.get("phno")
        doctor              = request.form.getlist('doctor')[0]
        appointment_date    = datetime.strptime(request.form['appointment_date'], '%Y-%m-%d').date()
        time_slot           = request.form.getlist('time_slot')[0]

        # change appointment date to string
        appointment_date = appointment_date.strftime("%d/%m/%Y")

        print(first_name, last_name, email, phone_number, doctor, appointment_date, time_slot)

        # insert data into database
        result = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "doctor": doctor,
            "appointment_date": appointment_date,
            "time_slot": time_slot
        }

        collection_name = 'health-care'
        new_collection = database[collection_name]
        x = new_collection.insert_one(result)
        print(x)

        return render_template('index.html')

    return render_template('patient_registration.html')

if __name__== "__main__":
    app.run(host="0.0.0.0", debug = True, port = PORT)