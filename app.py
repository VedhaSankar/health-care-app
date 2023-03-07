from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

from flask_pymongo import PyMongo,pymongo
from flask_mongoengine import MongoEngine

load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

PORT        = os.environ.get('PORT')
MONGO_URI   = os.environ.get('MONGO_URI')


mongo   = PyMongo(app)
db      = MongoEngine()
db.init_app(app)

users_obj               = mongo.db.users
patient_appointment_obj = mongo.db.patient_appointment


@app.route('/register', methods = ["GET", "POST"])
def register():

    if (request.method == "POST"):

        return redirect('/registration-successful')

    return render_template('register.html')


@app.route('/registration-successful', methods = ["POST"])
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

        # collection_name = 'users'
        # new_collection = database[collection_name]
        x = users_obj.insert_one(result)
        print(x)

        return render_template('register.html', message = "Registration Successful")
    
    return render_template('register.html')




@app.route('/', methods = ["GET", "POST"])
def index():

    if (request.method == "POST"):


        return redirect('/home')
    
    return render_template('index.html')


@app.route('/home', methods = ["GET", "POST"])
def home():


    return render_template('home.html')


@app.route('/login', methods = ["GET", "POST"])
def login():
        
    if (request.method == "POST"):

        user        = request.values.get("user")
        password    = request.values.get("password")

        user_from_db = users_obj.find_one({'username': user})

        print(user_from_db)

        if user_from_db:

            if password == user_from_db['password']:

                return render_template('home.html', message = "Login Successful")                
            
            else:
                    
                return render_template('login.html', message = "Incorrect password")
            
        else:
            
            return render_template('login.html', message = "Username not found")

    return render_template('login.html')


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

        # collection_name = 'patient-appointment'
        # new_collection = database[collection_name]
        x = patient_appointment_obj.insert_one(result)
        print(x)

        return render_template('patient_registration.html', message = "Appointment booked successfully")

    return render_template('patient_registration.html')



if __name__== "__main__":
    app.run(host="0.0.0.0", debug = True, port = PORT)
    # authenticate("vedha", "1234")