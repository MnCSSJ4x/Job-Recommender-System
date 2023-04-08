import json
from flask import Flask, redirect, request, session, jsonify
import firebase_admin
from firebase_admin import auth, credentials, firestore
from flask_cors import CORS, cross_origin
import requests


app = Flask(__name__)  # Initialze flask constructor
CORS(app, supports_credentials=True)
# Add your own details
config = {
    "apiKey": "AIzaSyCED9JBJpPI-O8m9Qulf42w3VxjzsD36r4",
    "authDomain": "recsys-219cb.firebaseapp.com",
    "projectId": "recsys-219cb",
    "storageBucket": "recsys-219cb.appspot.com",
    "messagingSenderId": "1088662279391",
    "appId": "1:1088662279391:web:85629515d441c9e543056a",
    "measurementId": "G-ZL1MTRH57Q",
    "databaseURL": ""
}

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
# Initialize the Firebase Admin SDK
cred = credentials.Certificate(
    'recsys-219cb-firebase-adminsdk-xp1fv-18a74f46aa.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
# doc_ref = db.collection(u'users').document(u'alovelace')
# doc_ref.set({
#     u'first': u'Ada',
#     u'last': u'Lovelace',
#     u'born': 1815
# })


@app.route('/signin', methods=['POST'])
@cross_origin(origins=['http://localhost:3001'])
def firebase_signin():
    # Verify the Firebase ID token
    token = request.json['token']
    # Verify the Firebase ID token to get the user ID and email
    decoded_token = auth.verify_id_token(token)
    uid = decoded_token['uid']
    email = decoded_token['email']
    custom_token = auth.create_custom_token(uid)
    custom_token_string = custom_token.decode()
    data = {
        'token': custom_token_string
    }
    # Convert the data to a JSON string
    data_json = json.dumps(data)
    # Set the headers for the POST request
    headers = {
        'Content-Type': 'application/json',
    }
    resp = requests.post(
        f'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key={config["apiKey"]}', data=data_json, headers=headers)
    data = resp.json()

    if 'error' in data:
        return jsonify({'error': data['error']['message']}), 400

    # Handling the response from the Firebase Authentication API
    users_ref = db.collection(u'users').document(uid).get()
    if users_ref.exists:
        return jsonify({'message': 'Successfully signed in!', 'userID': uid, 'firstTime': False})

    else:
        doc_ref = db.collection(u'users').document(uid)
        doc_ref.set({
            u'email': email,
            u'resume_extract': '',
        })
        return jsonify({'message': 'Successfully signed in!', 'userID': uid, 'firstTime': True})

    # db.collection
    # Return a response to the client


if __name__ == '__main__':
    # app.secret_key = 'YOUR_SECRET_KEY'
    app.run(debug=True)
