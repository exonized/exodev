import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {


  useEffect(() => {


    axios.get('http://localhost:8081/')
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.error(error);
      });

  }, []);



  return (
    <div>
      <h1>Hello from Readfdgfgfghft!</h1>
    </div>
  );
}

export default App;