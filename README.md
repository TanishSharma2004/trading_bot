# Binance Futures Trading Bot

A Python trading bot for Binance Futures Testnet with CLI interface.

## Features
- ✅ Market orders (BUY/SELL)
- ✅ Limit orders with price specification
- ✅ Real-time price checking
- ✅ Account balance monitoring
- ✅ Comprehensive error handling
- ✅ Detailed logging
- ✅ Input validation

## Setup Instructions

### Prerequisites
- Python 3.7+
- Binance Futures Testnet account
- API keys with Futures trading enabled

### Installation
1. Clone the repository:
```bash
git clone https://github.com/TanishSharma2004/trading_bot
cd trading-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file with your API credentials:
```
BINANCE_API_KEY=your_api_key_here (api_key from - https://testnet.binancefuture.com/en/futures/BTCUSDT)
BINANCE_API_SECRET=your_secret_key_here (api_secret from - https://testnet.binancefuture.com/en/futures/BTCUSDT)
```

4. Run the bot:
```bash
python main.py
```

## Usage

### Available Commands
- `test` - Test API connection
- `balance` - Show account balance
- `price` - Get current price for any symbol
- `limits` - Show price limits for symbol
- `market` - Place market order (immediate execution)
- `limit` - Place limit order (execute at specific price)
- `help` - Show command menu
- `quit` - Exit application

### Example Usage
```
Enter command: price
Enter symbol (e.g., BTCUSDT): BTCUSDT
💰 BTCUSDT current price: $43250.50

Enter command: market
📊 Market Order
Enter symbol (e.g., BTCUSDT): BTCUSDT
Enter side (BUY/SELL): BUY
Enter quantity: 0.001
✅ Market order placed successfully!
```

## Project Structure
```
trading_bot/
├── main.py          # Main CLI interface
├── bot.py           # Core trading bot logic
├── config.py        # Configuration settings
├── utils.py         # Utility functions
├── requirements.txt # Dependencies
├── logs/           # Log files directory
└── .env            # API credentials (not in repo)
```

## Safety Features
- Testnet-only operations
- Input validation for all parameters
- Comprehensive error handling
- Detailed logging of all operations
- API rate limiting awareness

## Technical Details
- **API**: Binance Futures Testnet
- **Library**: python-binance
- **Order Types**: Market, Limit
- **Symbols**: All USDT-M futures pairs
- **Logging**: File and console output

## Log Files
All operations are automatically logged to `logs/trading_bot.log` with timestamps and detailed information about:
- API requests and responses
- Order placements and results
- Error conditions and handling
- User interactions

### Understanding the Logs
The bot creates comprehensive logs that serve as a complete audit trail of all trading activities. Each log entry includes:

**Timestamp Format**: `2025-06-20 20:15:30,123`
**Log Levels**: 
- `INFO` - Successful operations (connections, orders, balance checks)
- `ERROR` - Failed operations or API errors
- `WARNING` - Unusual conditions that don't stop execution

**Sample Log Entries**:
```
2025-06-20 20:15:30,123 - utils - INFO - Bot initialized successfully
2025-06-20 20:15:31,456 - utils - INFO - API connection test successful
2025-06-20 20:15:45,789 - utils - INFO - Market order placed: {
    'orderId': 1234567890, 
    'symbol': 'BTCUSDT', 
    'side': 'BUY', 
    'origQty': '0.001',
    'status': 'FILLED'
}
2025-06-20 20:16:02,234 - utils - ERROR - Binance API error: Insufficient balance
```

### Log File Purpose
These logs are essential for:
- **Debugging**: Track down issues and understand bot behavior
- **Compliance**: Maintain records of all trading activities
- **Analysis**: Review trading patterns and performance
- **Verification**: Prove that the bot executed trades successfully

The log files are automatically created in the `logs/` directory when you first run the bot. No manual setup required!

## Author
Tanish Sharma
Email: tanish989130@gmail.com]
