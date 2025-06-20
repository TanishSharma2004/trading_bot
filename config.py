import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY', 'your_api_key_here')
API_SECRET = os.getenv('BINANCE_API_SECRET', 'your_secret_key_here')
TESTNET_URL = 'https://testnet.binancefuture.com'

# Trading Configuration
DEFAULT_SYMBOL = 'BTCUSDT'
DEFAULT_QUANTITY = 0.001  

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/trading_bot.log'