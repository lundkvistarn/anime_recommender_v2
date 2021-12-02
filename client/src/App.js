import React, { useState, useEffect } from "react";
import PostForm from "./components/PostForm";

function App() {
  const [data, setData] = useState([{}]);

  /*   useEffect(() => {
    fetch("/PostForm")
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        console.log(data);
      });
  }, []); */

  return (
    <div>
      <form action="#" method="post">
        <p>Name:</p>
        <input name="nm" type="text"></input>
        <input type="submit" value="submit"></input>
      </form>
    </div>
  );
}

export default App;
