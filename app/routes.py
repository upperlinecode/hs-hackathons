import os
from app import app
from flask import render_template, request, redirect
import pyrebase

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
user = auth.sign_in_with_email_and_password("danny@upperlinecode.com", "superstrongpw")


@app.route('/')
@app.route('/index')
@app.route('/hackathons')

def index():

    events = db.child("events").get(user['idToken']).val().values()
    # print(events.values())
    return render_template('index.html', events = events)

@app.route('/hackathons/new', methods=['GET', 'POST'])

def new_hackathon():
    if request.method == "GET":
        return render_template('new_hackathon.html')
    else:
        new_event = dict(request.form)
        db.child("events").push(new_event, user['idToken'])
        print(new_event)
        return redirect('hackathons')
