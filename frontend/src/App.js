import React, { useEffect, useState } from "react";

function App() {

  const [categories, setCategories] = useState([]);

  useEffect(() => {
    axios({
      method: 'get',
      url: urlapi + '/'
    })
      .then((response) => {

      })
      .catch(error => {
        console.log("ERROR: ", error);
      });

  }, []);

  return (
    <div>
      <h1>Hello from React!</h1>
      {categories}
    </div>
  );
}

export default App;