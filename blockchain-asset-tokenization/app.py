from flask import Flask, request, jsonify
from web3 import Web3
import json
import logging
from datetime import datetime
from functools import wraps
from blockchain_utils import BlockchainDataProvider

# Initialize Flask App
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Blockchain Data Provider
blockchain_provider = BlockchainDataProvider()

def validate_address(address):
    """Validate ethereum address format."""
    return Web3.is_address(address)

def require_valid_address(f):
    """Decorator to validate ethereum addresses in requests."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        address = request.args.get('address') or request.json.get('address')
        if not address or not validate_address(address):
            return jsonify({"error": "Invalid Ethereum address"}), 400
        return f(*args, **kwargs)
    return decorated_function

@app.route("/mint", methods=["POST"])
@require_valid_address
def mint_tokens():
    """
    Mint new tokens to a recipient's wallet.
    
    Request JSON:
    {
        "recipient": "0x...",
        "amount": number
    }
    """
    try:
        data = request.json
        recipient = data.get("recipient")
        amount = data.get("amount")

        if not isinstance(amount, (int, float)) or amount <= 0:
            return jsonify({"error": "Invalid amount"}), 400

        logger.info(f"Minting {amount} tokens to {recipient}")
        result = blockchain_provider.mint_tokens(recipient, int(amount))
        
        return jsonify({
            "transaction_hash": result["transaction_hash"],
            "status": result["status"],
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in mint_tokens: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/balance", methods=["GET"])
@require_valid_address
def get_balance():
    """
    Retrieve token balance of a specific wallet.
    
    Query Parameters:
    - address: Ethereum address to check balance
    """
    try:
        wallet_address = request.args.get("address")
        logger.info(f"Fetching balance for {wallet_address}")
        
        balance = blockchain_provider.get_token_balance(wallet_address)
        return jsonify({
            "wallet_address": wallet_address,
            "balance": balance,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in get_balance: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/transfer", methods=["POST"])
@require_valid_address
def transfer_tokens():
    """
    Transfer tokens between addresses.
    
    Request JSON:
    {
        "from_address": "0x...",
        "to_address": "0x...",
        "token_id": number
    }
    """
    try:
        data = request.json
        from_address = data.get("from_address")
        to_address = data.get("to_address")
        token_id = data.get("token_id")

        if not all([validate_address(from_address), validate_address(to_address)]):
            return jsonify({"error": "Invalid address format"}), 400

        if not isinstance(token_id, int) or token_id < 0:
            return jsonify({"error": "Invalid token ID"}), 400

        logger.info(f"Transferring token {token_id} from {from_address} to {to_address}")
        blockchain_provider.transfer_token(from_address, to_address, token_id)
        
        return jsonify({
            "status": "success",
            "message": f"Token {token_id} transferred successfully",
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in transfer_tokens: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/market/list", methods=["POST"])
@require_valid_address
def list_token_for_sale():
    """
    List a token for sale.
    
    Request JSON:
    {
        "token_id": number,
        "price": number
    }
    """
    try:
        data = request.json
        token_id = data.get("token_id")
        price = data.get("price")

        if not all([isinstance(token_id, int), isinstance(price, (int, float))]):
            return jsonify({"error": "Invalid token ID or price"}), 400

        if price <= 0:
            return jsonify({"error": "Price must be greater than 0"}), 400

        logger.info(f"Listing token {token_id} for sale at price {price}")
        blockchain_provider.list_token(token_id, int(price))
        
        return jsonify({
            "status": "success",
            "message": f"Token {token_id} listed for sale",
            "price": price,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in list_token_for_sale: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/market/buy", methods=["POST"])
@require_valid_address
def buy_listed_token():
    """
    Purchase a listed token.
    
    Request JSON:
    {
        "token_id": number
    }
    """
    try:
        data = request.json
        token_id = data.get("token_id")

        if not isinstance(token_id, int) or token_id < 0:
            return jsonify({"error": "Invalid token ID"}), 400

        logger.info(f"Purchasing token {token_id}")
        blockchain_provider.buy_token(token_id)
        
        return jsonify({
            "status": "success",
            "message": f"Token {token_id} purchased successfully",
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in buy_listed_token: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/tokens/search", methods=["GET"])
@require_valid_address
def search_owner_tokens():
    """
    Search for tokens owned by an address.
    
    Query Parameters:
    - address: Owner's Ethereum address
    """
    try:
        owner_address = request.args.get("address")
        logger.info(f"Searching tokens owned by {owner_address}")
        
        tokens = blockchain_provider.search_tokens_by_owner(owner_address)
        return jsonify({
            "owner_address": owner_address,
            "tokens": tokens,
            "count": len(tokens),
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in search_owner_tokens: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/burn", methods=["POST"])
@require_valid_address
def burn_token_endpoint():
    """
    Burn (destroy) a token.
    
    Request JSON:
    {
        "token_id": number
    }
    """
    try:
        data = request.json
        token_id = data.get("token_id")

        if not isinstance(token_id, int) or token_id < 0:
            return jsonify({"error": "Invalid token ID"}), 400

        logger.info(f"Burning token {token_id}")
        blockchain_provider.burn_token(token_id)
        
        return jsonify({
            "status": "success",
            "message": f"Token {token_id} burned successfully",
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in burn_token_endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/historical", methods=["GET"])
def get_historical_data():
    """
    Retrieve historical transaction data for tokens.
    
    Query Parameters:
    - start_date: ISO format date (YYYY-MM-DD)
    - end_date: ISO format date (YYYY-MM-DD)
    """
    try:
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if not start_date or not end_date:
            return jsonify({"error": "Start date and end date are required"}), 400

        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        logger.info(f"Fetching historical data from {start_date} to {end_date}")
        historical_data = blockchain_provider.get_historical_token_data(start_date, end_date)
        
        return jsonify({
            "historical_data": historical_data,
            "period": {"start": start_date, "end": end_date},
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in get_historical_data: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
    ##