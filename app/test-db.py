import pyrebase

config = {
  "apiKey": "AIzaSyBhbi5h7BKCGSVokkLDUBppvoEZYuogG-U",
  "authDomain": "hs-hackathons.firebaseapp.com",
  "databaseURL": "https://hs-hackathons.firebaseio.com",
  "projectId": "hs-hackathons",
  "storageBucket": "hs-hackathons.appspot.com",
  "serviceAccount": "hs-hackathons-firebase-adminsdk-w4k97-25ba3f70bb.json",
  "messagingSenderId": "1052538486567"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

#authenticate a user
user = auth.sign_in_with_email_and_password("danny@upperlinecode.com", "superstrongpw")



stuy = {"event_name": "Stuyhacks",
            "event_date":"1/1/2019",
            "event_website":"www.stuyhacks.com"}

db.child("events").push(stuy, user['idToken'])
