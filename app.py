from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()

PORT = os.environ.get('PORT')

app = Flask(__name__)

@app.route('/')
def start():

    return render_template('index.html')


@app.route('/patient-registration', methods = ["GET","POST"])
def patient_registration():

    return render_template('patient_registration.html')

if __name__== "__main__":
    app.run(host="0.0.0.0", debug = True, port = PORT)