import axios from "axios";
import Link from "next/link"
import { useEffect, useState } from "react"
import { useRouter } from "next/router";
import {BACKEND_HOME} from "../../constant" 
import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';
import 'firebase/compat/firestore';

const firebaseConfig = {
  "apiKey": "AIzaSyCED9JBJpPI-O8m9Qulf42w3VxjzsD36r4",
  "authDomain": "recsys-219cb.firebaseapp.com",
  "projectId": "recsys-219cb",
  "storageBucket": "recsys-219cb.appspot.com",
  "messagingSenderId": "1088662279391",
  "appId": "1:1088662279391:web:85629515d441c9e543056a",
  "measurementId": "G-ZL1MTRH57Q",
  "databaseURL": ""
}

if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig)
}

const Main = () => {
  const router = useRouter(); 
  const handleGoogleSignIn = () => {
    const provider = new firebase.auth.GoogleAuthProvider()
    firebase.auth().signInWithPopup(provider).then(function(result) {
      // User signed in successfully
      result.user!.getIdToken().then(function(idToken) {
        // Send the Firebase ID token to the backend server
        axios.post(BACKEND_HOME+'/signin', { token: idToken })
          .then(response => {
            //use response to move to next page 
            if(response.data.firstTime===true){
              router.push({pathname: '/welcome', query: { userID: response.data.userID}}); 
            }
            else{
              router.push({pathname: '/welcome', query: { userID: response.data.userID }}); 
              //goto different page 
              
            }
            console.log(response.data)
          })
          .catch(error => {
            console.log(error)
          })
      }).catch(function(error) {
        console.log(error)
      })
    }).catch(function(error) {
      console.log(error)
    })
  }
  
  return (
    <div>
        <section className="h-screen">
  <div className="h-full">
    {/* Left column container with background*/}
    <div className="g-6 flex h-full flex-wrap items-center justify-center lg:justify-between px-12">
      <div className="shrink-1 mb-12 grow-0 basis-auto md:mb-0 md:w-9/12 md:shrink-0 lg:w-6/12 xl:w-6/12">
        <img
          src="https://tecdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.webp"
          className="w-full"
          alt="Sample image"
        />
      </div>
      {/* Right column container */}
      <div className="mb-12 md:mb-0 md:w-8/12 lg:w-5/12 xl:w-5/12">
          {/*Description shit*/}
          <h1 className="relative mb-4 text-2xl font-black leading-tight text-white sm:text-4xl xl:mb-8">
          Welcome to our website! To sign-in using your Google account, please follow these simple steps:
      </h1>
    
          <div className="flex flex-row items-center justify-center lg:justify-start">
            
          <p className="mb-0 mr-4 font-black leading-tight text-gray-300 ">
          <li>Click on the "Sign In with Google" button below.</li>
<li>You will be redirected to a Google sign-in page.</li>
<li>Enter your Google email address and password. If prompted, grant permission for our website to access your Google account information.</li>
<li>You will be redirected back to our website and logged in automatically.</li>
<br/>
Thank you for choosing to sign-in with Google. It makes the registration process quick and easy!</p>
          </div>
          {/*Sign in section*/}
          <div className="flex flex-row items-center justify-center lg:justify-start mt-8">
            <p className="mb-0 mr-4 text-lg">Sign in with</p>
            <Link href="/">
                <button type="button" className="h-fullw-fulltext-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900" onClick={handleGoogleSignIn}>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="mx-auto h-3.5 w-3.5"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                 <path d="M15.545 6.558a9.42 9.42 0 0 1 .139 1.626c0 2.434-.87 4.492-2.384 5.885h.002C11.978 15.292 10.158 16 8 16A8 8 0 1 1 8 0a7.689 7.689 0 0 1 5.352 2.082l-2.284 2.284A4.347 4.347 0 0 0 8 3.166c-2.087 0-3.86 1.408-4.492 3.304a4.792 4.792 0 0 0 0 3.063h.003c.635 1.893 2.405 3.301 4.492 3.301 1.078 0 2.004-.276 2.722-.764h-.003a3.702 3.702 0 0 0 1.599-2.431H8v-3.08h7.545z"/>
              </svg>
            </button></Link>
        
          </div>

      </div>
    </div>
  </div>
</section>

  </div>
  )
}

export default Main