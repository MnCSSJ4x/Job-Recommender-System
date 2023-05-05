import React from 'react'
import { useState } from 'react';
import axios from 'axios';
import {BACKEND_HOME} from "../../constant" 
import { useRouter } from 'next/router';
const Main = () => {
    const [selectedOption, setSelectedOption] = useState("5");
    const router = useRouter(); 
    const uid:any = router.query.userID; 
    
    const handleSelectChange = (event: { target: { value: React.SetStateAction<string>; }; }) => {
        setSelectedOption(event.target.value);
    };

    const handleClick = (event: { preventDefault: () => void; })=>{
        console.log('Selected option: ',selectedOption);
        event.preventDefault();
        let formData = new FormData();
   
        formData.append('sentBy',uid?.toString());
        formData.append('number',selectedOption); 
        axios.post(BACKEND_HOME+'/getRecommendation', formData).then((response)=>{
          console.log(response);
            router.push({pathname: '/recommendation', query: { userID: response.data.userID, recommendations:response.data.recommendations }}); 
    }).catch(error => {
      console.log(error)
    })
        
    }
  return (
    <div>
        <section className="h-screen">
<div className="h-full">
{/* Left column container with resume upload*/}
<div className="g-6 flex h-full flex-wrap items-center justify-center lg:justify-between px-12">
  <div className="shrink-1 mb-12 grow-0 basis-auto md:mb-0 md:w-9/12 md:shrink-0 lg:w-6/12 xl:w-6/12">
     {/*Description shit*/}
     <h1 className="relative mb-4 text-2xl font-black leading-tight text-white sm:text-4xl xl:mb-8">
      One step away from landing your dream job!
  </h1>

      <div className="flex flex-row items-center justify-center lg:justify-start">
        
      <p className="mb-0 mr-4 font-black leading-tight text-gray-300 ">
     Your data is parsed and ready and all you need to tell us is the number of recommendations you want to see</p>
      </div>
      {/*Sign in section*/}
      
      
  

  </div>
  {/* Right column container */}
  <div className="mb-12 md:mb-0 md:w-8/12 lg:w-5/12 xl:w-5/12">
  <div className="flex items-center justify-center w-full">
  <label
    htmlFor="Number of recommendation"
    className="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-400"
  >
    Select an option
  </label>
  <select
    id="countries"
    value={selectedOption}
    onChange={handleSelectChange}
    className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
  >
    <option value="5">Five</option>
    <option value="10">Ten</option>
    <option value="20">Twenty</option>
    <option value="30">Thirty</option>
    <option value="50">Fifty</option>
  </select>

  <button type="submit" className="my-2 mx-2 h-fullw-fulltext-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900" onClick={handleClick}>
                Submit 
        </button>


</div>

  </div>
</div>
</div>
</section>

   </div>
  )
}

export default Main