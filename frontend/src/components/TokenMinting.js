import React, { useState } from "react";

function TokenMinting() {
    const [recipient, setRecipient] = useState("");
    const [amount, setAmount] = useState("");
  
    const handleMint = async () => {
      const response = await fetch("http://localhost:5000/mint", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ recipient, amount }),
      });
      const data = await response.json();
      alert(`Transaction Hash: ${data.tx_hash}`);
    };