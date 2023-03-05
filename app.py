from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime


load_dotenv()

PORT        = os.environ.get('PORT')
MONGO_URI   = os.environ.get('MONGO_URI')

client      = MongoClient(MONGO_URI)  
DB_NAME     = 'trials'
database    = client[DB_NAME]

app = Flask(__name__)


def authenticate(username, password):
    # check if user exists in database
    collection_name = 'health-care'
    collection = database[collection_name]


    user_found      = collection.find_one({"username": username})
    password_found  = collection.find_one({"password": password})

    # check if user exists in database
    if user_found and password_found:

        return True

    return False


@app.route('/register', methods = ["GET", "POST"])
def register():

    if (request.method == "POST"):

        return redirect('/registered')
    
    return render_template('register.html')


@app.route('/home', methods = ["POST"])
def registered():

    if (request.method == "POST"):

        # get user input from html form
        username            = request.values.get("username")
        first_name          = request.values.get("first_name")
        last_name           = request.values.get("last_name")
        email               = request.values.get("email")
        phone_number        = request.values.get("phno")
        password            = request.values.get("psw")


        # insert data into database
        result = {
            "username": username,   
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "password": password
        }

        collection_name = 'users'
        new_collection = database[collection_name]
        x = new_collection.insert_one(result)
        print(x)

        return render_template('register.html', message = "Registration Successful")

    return render_template('register.html')


@app.route('/', methods = ["GET", "POST"])
def login():

    if (request.method == "POST"):


        return redirect('/home')
    
    return render_template('login.html')



@app.route('/home', methods = ["POST"])
def home():

    user        = request.values.get("user")
    password    = request.values.get("password")

    if user == "admin" and password == "admin":

        return render_template('index.html', message = "Login Successful")

    return render_template('error.html')


@app.route('/patient-appointment-registration', methods = ["GET", "POST"])
def patient_appointment_registration():

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

        # print(first_name, last_name, email, phone_number, doctor, appointment_date, time_slot)

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

        collection_name = 'patient-appointment'
        new_collection = database[collection_name]
        x = new_collection.insert_one(result)
        print(x)

        return render_template('patient_registration.html', message = "Appointment booked successfully")

    return render_template('patient_registration.html')



if __name__== "__main__":
    app.run(host="0.0.0.0", debug = True, port = PORT)