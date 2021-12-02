import React, { useState, useEffect } from "react";
import PostForm from "./components/PostForm";

function App() {
  const [currentTime, setCurrentTime] = useState(0);
  const [currentTime2, setCurrentTime2] = useState(0);
  const [currentTime3, setCurrentTime3] = useState(null);

  useEffect(() => {
    fetch('/synopsis?name=Naruto&title=Test').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
      setCurrentTime2(data.name);
      setCurrentTime3(JSON.parse(data.name));
      console.log(JSON.parse(data.name));
    });
  }, []);

  return (
    <div>
      <form action="#" method="post">
        <p>Name:</p>
        <input name="nm" type="text"></input>
        <input type="submit" value="submit"></input>
        <p>{currentTime}</p>
        <p>{currentTime2}</p>
      </form>
    </div>
  );
}

export default App;
