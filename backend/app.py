from flask import Flask, request, jsonify
from web3 import Web3
import json
from blockchain_utils import BlockchainDataProvider
# Initialize Flask App
app = Flask(__name__)

# Initialize Blockchain Data Provider
blockchain_provider = BlockchainDataProvider()