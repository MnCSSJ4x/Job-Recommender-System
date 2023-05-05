import { useRouter } from 'next/router';
import React, { ReactNode, useEffect, useState } from 'react'
import Jobcard from './recommendation/components/jobcard';

const Recommendation = () => {
    const router = useRouter(); 
    const uid:any = router.query.userID; 
    let recommendations = JSON.parse(router.query.recommendations)

    const cardComponents = recommendations.map((item: any,index: any)=>{
      console.log(item);
      return (<div className='py-4'> <Jobcard data = {item} id={index}/></div>);
      
    })
  
  return (
    <div className='px-8 flex flex-col'>  
    <h1 className='py-4 text-4xl font-bold text-center'>Our Suggestions For You</h1>     
          {cardComponents}
    </div>
  )
}

export default Recommendation