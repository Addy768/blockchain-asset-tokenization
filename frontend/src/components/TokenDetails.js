import React, { useState } from "react";

function TokenDetails() {
    const [address, setAddress] = useState("");
    const [balance, setBalance] = useState("");
    const fetchBalance = async () => {
        const response = await fetch(`http://localhost:5000/balance?address=${address}`);
        const data = await response.json();
        setBalance(data.balance);
      };