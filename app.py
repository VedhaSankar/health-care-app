from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_session import Session
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from flask_mail import Mail, Message
from emailer import send_email
# from werkzeug import secure_filename
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
mail= Mail(app)


SENDER_ADDRESS  = os.environ.get('GMAIL_USER')
SENDER_PASS     = os.environ.get('GMAIL_PASSWORD')
EMAIL_LIST      = os.environ.get('EMAIL_LIST').split(',')
ALLOWED_EXTENSIONS  = {'pdf'}

app.secret_key =  b'_5#y2L"F4Q8z\n\xec]/4'

app.config['MAIL_SERVER']   ='smtp.gmail.com'
app.config['MAIL_PORT']     = 465
app.config['MAIL_USERNAME'] = SENDER_ADDRESS
app.config['MAIL_PASSWORD'] = SENDER_PASS
app.config['MAIL_USE_TLS']  = False
app.config['MAIL_USE_SSL']  = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = "uploads/"



PORT            = os.environ.get('PORT')
MONGO_URI       = os.environ.get('MONGO_URI')
DB_NAME         = os.environ.get('DB_NAME')

# creating a MongoClient object
client = MongoClient(MONGO_URI)

# accessing the database
database = client[DB_NAME]


def allowed_file(filename):

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/register', methods = ["GET", "POST"])
def register():

    if (request.method == "POST"):

        return redirect('/registration-successful')

    return render_template('patient_register.html')


@app.route('/registration-successful', methods = ["POST"])
def registered():

    if (request.method == "POST"):


        collection_name = 'users'
        new_collection = database[collection_name]

        # get user input from html form
        username            = request.values.get("username")
        first_name          = request.values.get("first_name")
        last_name           = request.values.get("last_name")
        email               = request.values.get("email")
        phone_number        = request.values.get("phno")
        password            = request.values.get("psw")
        role                = request.form.getlist('roles')[0]

        # get last inserted id
        try:
            id = new_collection.find().sort("_id", -1).limit(1)[0]['_id'] + 1
        except:
            id = 1

        # insert data into database
        result = {
            "_id": id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "password": password,
            "role": role
        }

        x = new_collection.insert_one(result)
        print(x)


        # Save the form data to the session object
        session['id'] = id
        # print(session['username'])

        return render_template('patient_register.html', message = "Registration Successful")

    return render_template('patient_register.html')




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

        username    = request.values.get("user")
        password    = request.values.get("password")

        collection_name = 'users'
        new_collection = database[collection_name]

        user_from_db = new_collection.find_one({'username': username})

        # print(user_from_db)

        if user_from_db:


            if password == user_from_db['password']:


                id = user_from_db['_id']
                session['id'] = id

                print(f"User ID {id} set to session")

                return render_template('home.html', message = "Login Successful")

            else:

                return render_template('login.html', message = "Incorrect password")

        else:

            return render_template('login.html', message = "Username not found")

    return render_template('login.html')


@app.route('/logout', methods = ["GET", "POST"])
def logout():

    session.pop('id', None)

    return render_template('index.html')


@app.route('/appointment-registration', methods = ["GET", "POST"])
def appointment_reg():

    if (request.method == "POST"):

        # get user input from html form
        print('lol')
        first_name          = request.values.get("first_name")
        last_name           = request.values.get("last_name")
        doctor              = request.form.getlist('doctor')[0]
        appointment_date    = datetime.strptime(request.form['appointment_date'], '%Y-%m-%d').date()
        time_slot           = request.form.getlist('time_slot')[0]

        # change appointment date to string
        appointment_date = appointment_date.strftime("%d/%m/%Y")

        # get user details from database
        collection_name = 'users'
        users_collection = database[collection_name]

        user_from_db = users_collection.find_one({'_id': session['id']})


        id                   = session['id']
        username_from_db     = user_from_db['username']

        collection_name = 'patient-appointment'
        patient_collection = database[collection_name]
        appointment_from_db = patient_collection.find({},{"appointment_date":1, "time_slot" : 1, "doctor" : 1})

        for item in appointment_from_db:

            if item['appointment_date'] == appointment_date and item["time_slot"] == time_slot and item['doctor'] == doctor:

                message = "Please choose a different time slot/date or choose a different doctor"

                return render_template("appointment-reg.html", message = message)

        result = {
            "user_id"           : id,       #connects user db to patient registration db
            "username"          : username_from_db,
            "first_name"        : first_name,
            "last_name"         : last_name,
            "doctor"            : doctor,
            "appointment_date"  : appointment_date,
            "time_slot"         : time_slot
        }

        x = patient_collection.insert_one(result)

        # print(x)

        message = f'Hello {first_name} {last_name}!\nYour appointment has been booked successfully. \nDoctor: {doctor} \nAppointment Date: {appointment_date} \nTime Slot: {time_slot}'


        # for sender in EMAIL_LIST:
        #     send_email(
        #     receiver_address=user_from_db['email'],
        #     subject='Appointment Confirmation',
        #     content=message
        #     )


        return redirect('/appointment-list')


    return render_template('appointment-reg.html')


@app.route('/appointment-list', methods = ["GET", "POST"])
def appointment_list():

    # print(session['id'])

    collection_name = 'patient-appointment'
    new_collection = database[collection_name]

    user_from_db = new_collection.find({'user_id': session['id']}, {"appointment_date" : 1, "time_slot":1, "doctor":1, "first_name":1, "last_name":1})

    return render_template('appointment-list.html',user_from_db = user_from_db)


@app.route('/appointments', methods = ["GET", "POST"])
def appointments():

    # list all apopointments for a user
    # modify appointment
    # get report

    return render_template('appointments-master-page.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():

    if request.method == 'POST':

        if 'file' not in request.files:

            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        print(file)

        if file.filename == '':

            print("bro")

            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('upload.html', message="File uploaded successfully")

        else:
            flash('Allowed file type is .pdf')
            return redirect(request.url)

    return render_template('upload.html')


# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_file():
#    if request.method == 'POST':
#       f = request.files['file']
#       filename = secure_filename(f.filename)
#       f.save(app.config['UPLOAD_FOLDER'] + filename)
#       return 'file uploaded successfully'
#    return render_template('upload.html')



@app.route('/feedback', methods = ['GET', 'POST'])
def feedback():


   if request.method == 'POST':

       collection_name = 'feedback'

       new_collection = database[collection_name]

       feedback       = request.values.get("feedback")

       result = {
           "feedback":feedback
       }
       x=new_collection.insert_one(result)
       print(x)
       return render_template('feedback.html',message='Thank you for your feedback!')
   return render_template('feedback.html')


@app.route('/modify-appointment', methods = ['GET', 'POST'])
def modify_appointment():

    if request.method == 'POST':
       patient_name             = request.values.get("patient-name")
       old_appointment_date     = datetime.strptime(request.form['old-appointment-date'], '%Y-%m-%d').date()
       old_appointment_time     = request.form.getlist('old-appointment-time')[0]
       new_appointment_date     = datetime.strptime(request.form['new-appointment-date'], '%Y-%m-%d').date()
       new_appointment_time     = request.form.getlist('new-appointment-time')[0]
       doctor                   = request.values.getlist("doctor")[0]

       old_appointment_date     = old_appointment_date.strftime("%d/%m/%Y")
       new_appointment_date     = new_appointment_date.strftime("%d/%m/%Y")

       collection_name          = 'patient-appointment'
       patient_collection       = database[collection_name]

       appointment_from_db      = patient_collection.find({},{"appointment_date":1, "time_slot" : 1, "doctor" : 1})

       for item in appointment_from_db:

            if item['appointment_date'] == new_appointment_date and item["time_slot"] == new_appointment_time and item['doctor'] == doctor:

                message = "Please choose a different time slot/date or choose a different doctor"

                return render_template("modify-appointment.html", message = message)

            else:

                condition = { "first_name": patient_name }
                update_new = { "$set": { "appointment_date": new_appointment_date, "time_slot": new_appointment_time } }


                patient_collection.update_one(condition, update_new)

                # patient_collection.update(myquery, newvalues)

            return render_template("modify-appointment.html", message="Appointment modified successfully")

    return render_template("modify-appointment.html")


if __name__== "__main__":

    app.run(host="0.0.0.0", debug = True, port = PORT)
    # authenticate("vedha", "1234")