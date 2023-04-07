import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyCED9JBJpPI-O8m9Qulf42w3VxjzsD36r4",
    "authDomain": "recsys-219cb.firebaseapp.com",
    "projectId": "recsys-219cb",
    "storageBucket": "recsys-219cb.appspot.com",
    "messagingSenderId": "1088662279391",
    "appId": "1:1088662279391:web:85629515d441c9e543056a",
    "measurementId": "G-ZL1MTRH57Q",
    "databaseURL": ""
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
