import React, { useState, useEffect } from "react";

function App() {
  const [data, setData] = useState([{}]);

  useEffect(() => {
    fetch("/practice")
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        console.log(data);
      });
  }, []);
  return (
    <div>
      {typeof data.practice === "undefined" ? (
        <p>Loading...</p>
      ) : (
        data.practice.map((number, i) => <p key={i}>{number}</p>)
      )}
    </div>
  );
}

export default App;
