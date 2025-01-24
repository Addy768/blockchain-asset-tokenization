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
    return (
        <div>
          <h2>Mint Tokens</h2>
          <input
            type="text"
            placeholder="Recipient Address"
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
          />
          <input
            type="number"
            placeholder="Amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
          />
          <button onClick={handleMint}>Mint</button>
        </div>
      );
    }
    
    export default TokenMinting;