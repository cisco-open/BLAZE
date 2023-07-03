import React from "react";
import logo from "../logo.svg";
export function Sidebar({ children }) {
  return (
    <>
      
      <div
        className="d-flex flex-column flex-shrink-0 justify-content-between p-3 text-white bg-dark"
        style={{ width: 280 }}
      >
       <div>
       {children}
       </div> 
        
        <img src={"./ciscoLogo.png"} alt="Cisco Logo" style={{paddingBottom:"1rem"}}/>


       
      </div>
    </>
  );
}
