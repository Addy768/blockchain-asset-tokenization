import React from "react";
import Header from "./components/Header";
import TokenMinting from "./components/TokenMinting";
import TokenDetails from "./components/TokenDetails";

function App() {
    return (
      <div>
        <Header />
        <TokenMinting />
        <TokenDetails />
      </div>
    );
  }
  
  export default App;