import logging
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

def setup_logging():
    """Setup logging configuration"""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/trading_bot.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def print_colored(message, color=Fore.WHITE):
    """Print colored messages to terminal"""
    print(f"{color}{message}{Style.RESET_ALL}")

def validate_symbol(symbol):
    """Validate trading symbol format"""
    if not symbol or not isinstance(symbol, str):
        return False
    return symbol.upper().endswith('USDT')

def validate_quantity(quantity):
    """Validate order quantity"""
    try:
        qty = float(quantity)
        return qty > 0
    except (ValueError, TypeError):
        return False