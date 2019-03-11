import os
from app import app
from flask import render_template, request, redirect, session
import pyrebase

app.secret_key = os.environ['SECRET_KEY']


config = {
  "apiKey": os.environ['FIREBASE_APIKEY'],
  "authDomain": "hs-hackathons.firebaseapp.com",
  "databaseURL": "https://hs-hackathons.firebaseio.com",
  "projectId": "hs-hackathons",
  "storageBucket": "hs-hackathons.appspot.com",
  "serviceAccount": "app/firebase-private-key.json",
  "messagingSenderId": "1052538486567"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()
#authenticate a user

@app.route('/')
@app.route('/index')
@app.route('/hackathons')

def index():
    events = db.child("events").get().val().values()
    #This is not working. How to check if a user is logged in??? it is not finding the user variable
    if 'user' in session:
        return render_template('index.html', events = events, user=session['user']['email'])
    else:
        print("no user")
        return render_template('index.html', events = events)

# CREATING A NEW EVENT

@app.route('/hackathons/new', methods=['GET', 'POST'])

def new_hackathon():
    if request.method == "GET":
        return render_template('new_hackathon.html')
    else:
        new_event = dict(request.form)
        user = session['user']
        db.child("events").push(new_event, user['idToken'])
        print(new_event)
        return redirect('hackathons')

# SIGNING UP - creates a new user in firebase

@app.route('/sign-up', methods=['GET', 'POST'])

def sign_up():
    if request.method == "GET":
        return render_template('sign_up.html')
    else:
        new_user = dict(request.form)
        try:
            user = auth.create_user_with_email_and_password(new_user["email"], new_user["password"])
            session['user'] = user
        except:
            print("unable to create account")
        return redirect('hackathons')

# LOGGING IN - logs in

@app.route('/log-in', methods=['GET', 'POST'])

def log_in():
    session
    if request.method == "GET":
        return render_template('log_in.html')
    else:
        logging_in_user = dict(request.form)
        try:
            user = auth.sign_in_with_email_and_password(logging_in_user["email"], logging_in_user["password"])
            session['user'] = user
        except:
            print("unable to log in")
        return redirect('hackathons')


@app.route('/log-out')

def log_out():
    session.pop('user', None)
    return redirect('hackathons')
