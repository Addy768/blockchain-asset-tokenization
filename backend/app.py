from flask import Flask, request, jsonify
from web3 import Web3
import json
from blockchain_utils import BlockchainDataProvider
# Initialize Flask App
app = Flask(__name__)

# Initialize Blockchain Data Provider
blockchain_provider = BlockchainDataProvider()

@app.route("/mint", methods=["POST"])
def mint_tokens():
    """
    Mint new tokens to a recipient's wallet.
    Expects JSON payload with 'recipient' and 'amount'.
    """
    try:
        data = request.json
        recipient = data.get("recipient")
        amount = data.get("amount")

        if not recipient or not amount:
            return jsonify({"error": "Recipient and amount are required"}), 400

        # Mint tokens
        result = blockchain_provider.mint_tokens(recipient, int(amount))
        return jsonify({
            "transaction_hash": result["transaction_hash"],
            "status": result["status"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/balance", methods=["GET"])