import React from 'react'
import {BACKEND_HOME} from "../../constant" 
import axios from 'axios';
import { useState } from 'react';
const Main = () => {
  const [file, setFile] = useState<File>();

  const handleFileChange = (event:any) => {
    console.log(event.target)
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event:any) => {
    event.preventDefault();
    let formData = new FormData();
   
    formData.append('sentBy','monjoy')
    formData.append('file', file!);
    axios.post(BACKEND_HOME+'/upload', formData).then(()=>{
      console.log("TIS DONE")
    }).catch(error => {
      console.log(error)
    })
    
  };
  return (
    <div>
    <section className="h-screen">
<div className="h-full">
{/* Left column container with resume upload*/}
<div className="g-6 flex h-full flex-wrap items-center justify-center lg:justify-between px-12">
  <div className="shrink-1 mb-12 grow-0 basis-auto md:mb-0 md:w-9/12 md:shrink-0 lg:w-6/12 xl:w-6/12">
  <div className="flex items-center justify-center w-full">
  <form onSubmit={handleSubmit}>
      <input type="file" onChange={handleFileChange} />
      <button type="submit" className="h-fullw-fulltext-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900">
                Submit 
        </button>
  </form>
  
    {/* <input id="dropzone-file" type="file" className="hidden" formAction='/uploader' /> */}

</div>

  </div>
  {/* Right column container */}
  <div className="mb-12 md:mb-0 md:w-8/12 lg:w-5/12 xl:w-5/12">
      {/*Description shit*/}
      <h1 className="relative mb-4 text-2xl font-black leading-tight text-white sm:text-4xl xl:mb-8">
      Lets get started!!! 
  </h1>

      <div className="flex flex-row items-center justify-center lg:justify-start">
        
      <p className="mb-0 mr-4 font-black leading-tight text-gray-300 ">
      Welcome to our solution! To get started, please upload your resume using the form below. Your resume should be in PDF format and include your work experience, education, and any relevant skills or certifications. This will help us to find relevant jobs and recommend you the best fit!</p>
      </div>
      {/*Sign in section*/}
      

  </div>
</div>
</div>
</section>

</div>
  )
}

export default Main;