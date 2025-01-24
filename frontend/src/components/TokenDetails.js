import React, { useState } from "react";

function TokenDetails() {
    const [address, setAddress] = useState("");
    const [balance, setBalance] = useState("");
    const fetchBalance = async () => {
        const response = await fetch(`http://localhost:5000/balance?address=${address}`);
        const data = await response.json();
        setBalance(data.balance);
      };
      return (
        <div>
          <h2>Check Balance</h2>
          <input
            type="text"
            placeholder="Wallet Address"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
          />
          <button onClick={fetchBalance}>Check</button>
          {balance && <p>Balance: {balance}</p>}
        </div>
      );
    }