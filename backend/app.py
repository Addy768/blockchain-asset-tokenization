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
def get_balance():
    """
    Retrieve token balance of a specific wallet.
    Expects 'address' as a query parameter.
    """
    try:
        wallet_address = request.args.get("address")
        if not wallet_address:
            return jsonify({"error": "Wallet address is required"}), 400

        # Get balance
        balance = blockchain_provider.get_token_balance(wallet_address)
        return jsonify({
            "wallet_address": wallet_address,
            "balance": balance
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    # sss

@app.route("/historical", methods=["GET"])
def get_historical_data():
    """ 
    Retrieve historical transaction data for tokens.
    Expects 'start_date' and 'end_date' as query parameters.
    """
    try:
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if not start_date or not end_date:
            return jsonify({"error": "Start date and end date are required"}), 400

        # Fetch historical data (functionality needs implementation in blockchain_utils.py)
        historical_data = blockchain_provider.get_historical_token_data(start_date, end_date)
        return jsonify({"historical_data": historical_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)