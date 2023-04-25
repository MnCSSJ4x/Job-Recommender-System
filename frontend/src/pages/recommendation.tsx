import { useRouter } from 'next/router';
import React, { useEffect, useState } from 'react'
import Jobcard from './recommendation/components/jobcard';

const Recommendation = () => {
    const router = useRouter(); 
    const uid:any = router.query.userID; 
    let {recommendations} = router.query;
    const data:Array<Object> = JSON.parse(recommendations)  as Array<Object>; ;
  return (
    <div>
        <div className=''>
           {
                data.map(()=>{
                    <div>
                        HI
                    </div>
                })
           }
        </div>
    </div>
  )
}

export default Recommendation