import json
from flask import Flask, redirect, request, session, jsonify
import firebase_admin
from firebase_admin import auth, credentials
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


@app.route('/signin', methods=['POST'])
@cross_origin(origins=['http://localhost:3001'])
def firebase_signin():
    # Verify the Firebase ID token
    token = request.json['token']
    # Verify the Firebase ID token to get the user ID and email
    decoded_token = auth.verify_id_token(token)
    uid = decoded_token['uid']
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
    print(data)
    if 'error' in data:
        return jsonify({'error': data['error']['message']}), 400
    print(data)
    # Handling the response from the Firebase Authentication API

    # Return a response to the client
    return jsonify({'message': 'Successfully signed in!'})


if __name__ == '__main__':
    # app.secret_key = 'YOUR_SECRET_KEY'
    app.run(debug=True)
