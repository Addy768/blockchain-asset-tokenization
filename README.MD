# Blockchain Asset Tokenization API

A Flask-based REST API for managing tokenized assets on the Ethereum blockchain. This project enables secure minting, trading, and management of digital assets through a simple HTTP interface.

## Features

- Token Management
  - Mint new tokens
  - Check token balances
  - Transfer tokens between wallets
  - Burn tokens

- Marketplace Functions
  - List tokens for sale
  - Purchase listed tokens
  - Search tokens by owner
  
- Historical Data
  - Track token transactions
  - View historical ownership data
  - Monitor price history

## Prerequisites

- Python 3.8+
- Ganache or other Ethereum node
- Web3 provider (local or remote)
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Addy768/blockchain-asset-tokenization.git
cd blockchain-asset-tokenization
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```env
CONTRACT_ADDRESS=your_contract_address
PROVIDER_URL=http://127.0.0.1:7545
```

## Configuration

1. Update `blockchain_utils.py` with your contract's ABI:
```python
self.contract_abi = [
    # Your contract ABI here
]
```

2. Configure your Web3 provider in `.env`
3. Set your contract address in `.env`

## Usage

1. Start the server:
```bash
python app.py
```

2. The API will be available at `http://localhost:5000`

### API Endpoints

#### Token Operations

```http
POST /mint
Content-Type: application/json

{
    "recipient": "0x...",
    "amount": 100
}
```

```http
GET /balance?address=0x...
```

```http
POST /transfer
Content-Type: application/json

{
    "from_address": "0x...",
    "to_address": "0x...",
    "token_id": 1
}
```

#### Marketplace Operations

```http
POST /market/list
Content-Type: application/json

{
    "token_id": 1,
    "price": 1000000000000000000  # Price in wei
}
```

```http
POST /market/buy
Content-Type: application/json

{
    "token_id": 1
}
```

```http
GET /tokens/search?address=0x...
```

#### Historical Data

```http
GET /historical?start_date=2024-01-01&end_date=2024-01-31
```

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Successful operation
- 400: Invalid input
- 500: Server error

Error responses include detailed messages:
```json
{
    "error": "Description of the error",
    "timestamp": "2024-01-27T12:00:00Z"
}
```

## Security Features

- Ethereum address validation
- Input sanitization
- Transaction verification
- Error logging
- Request rate limiting (configurable)

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository.

## Acknowledgments

- Web3.py documentation
- Flask documentation
- Ethereum community resources
