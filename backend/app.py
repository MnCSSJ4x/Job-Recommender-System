import json
from flask import Flask, redirect, request, session, jsonify
import firebase_admin
from firebase_admin import auth, credentials, firestore
from flask_cors import CORS, cross_origin
import requests
import os
from pyresparser import ResumeParser
import tempfile
import pathlib
from rankingNetwork import * 
import pandas as pd


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



@app.route('/signin', methods=['POST'])
@cross_origin(origins=['*'])
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


@app.route('/upload', methods=['POST'])
@cross_origin(origins=['*'])
def handle_upload_parse_resume():
    # print(request.form)
    # print(request.files)
    file = request.files['file']
    filename = file.filename
    # Convert flask file to a pathfile for pyresparser
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        file.save(tmp.name+'.pdf')
        path = pathlib.Path(tmp.name+'.pdf')
        data = ResumeParser(str(path)).get_extracted_data()

    uid = request.form['sentBy']
    users_ref = db.collection(u'users').document(uid)

    if users_ref.get().exists:
        users_ref.update({
            'resume_extract': data
        })
        

    else:
        return jsonify({'message': 'File uploaded successfully, Parsing done, Firebase error - User Doesnt exist'})

    # Save the file to the cache directory
    return jsonify({'message': 'File uploaded successfully and parsed','userID':uid})

@app.route('/getRecommendation',methods=['POST'])
@cross_origin(origins=['*'])
def getRecommendation():
    #get user info 
    uid = request.form['sentBy']
    k =int( request.form['number'])
    users_ref = db.collection(u'users').document(uid)
    if users_ref.get().exists:
       user_data = users_ref.get().to_dict()
       skillset = user_data['resume_extract']['skills']
       skillset = ' '.join(skillset)
       CosineMatrix,merged_df = getCosineMatrix(skillset)
       merged_df.drop(columns=["tensor1","tensor2","cosine_similarity"],inplace=True)
       subset = merged_df.iloc[0:k]
       json_data = subset.to_json(orient='records')
       return jsonify({'message': 'Recommendation obtained succesfully', 'recommendations':json_data, 'userID':uid})
    
    else:
        return jsonify({'message': 'User Doesnt exist'})



if __name__ == '__main__':
    # app.secret_key = 'YOUR_SECRET_KEY'
    app.run(debug=True)
