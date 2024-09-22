import React, { createContext, useState } from 'react'

const LoginContext = createContext();

 export const LoginProvider = ({children})=>{

    const [LoggedAs , SetLoggedAs] = useState('')


    return(
       <LoginContext.Provider value={{LoggedAs,SetLoggedAs}}>

        {children}

       </LoginContext.Provider>
    )
 }


 


export default LoginContext
