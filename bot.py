from binance import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import logging
from utils import print_colored, setup_logging
from config import API_KEY, API_SECRET
from colorama import Fore

class BasicBot:
    def __init__(self, api_key=API_KEY, api_secret=API_SECRET, testnet=True):
        """Initialize the trading bot"""
        self.logger = setup_logging()
        
        try:
            self.client = Client(api_key, api_secret, testnet=testnet)
            self.client.API_URL = 'https://testnet.binancefuture.com/fapi/v1'
            self.logger.info("Bot initialized successfully")
            print_colored("✅ Bot initialized successfully!", Fore.GREEN)
        except Exception as e:
            self.logger.error(f"Failed to initialize bot: {str(e)}")
            print_colored(f"❌ Failed to initialize bot: {str(e)}", Fore.RED)
            raise

    def test_connection(self):
        """Test API connection"""
        try:
            account_info = self.client.futures_account()
            self.logger.info("API connection test successful")
            print_colored("✅ API connection successful!", Fore.GREEN)
            return True
        except Exception as e:
            self.logger.error(f"API connection failed: {str(e)}")
            print_colored(f"❌ API connection failed: {str(e)}", Fore.RED)
            return False

    def get_account_balance(self):
        """Get account balance"""
        try:
            account = self.client.futures_account()
            balances = account['assets']
            
            print_colored("\n💰 Account Balances:", Fore.CYAN)
            for balance in balances:
                if float(balance['walletBalance']) > 0:
                    print(f"  {balance['asset']}: {balance['walletBalance']}")
            
            return balances
        except Exception as e:
            self.logger.error(f"Failed to get balance: {str(e)}")
            print_colored(f"❌ Failed to get balance: {str(e)}", Fore.RED)
            return None

    def get_symbol_info(self, symbol):
        """Get symbol trading information"""
        try:
            exchange_info = self.client.futures_exchange_info()
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol.upper():
                    return s
            return None
        except Exception as e:
            self.logger.error(f"Failed to get symbol info: {str(e)}")
            return None

    def place_market_order(self, symbol, side, quantity):
        """Place market order"""
        try:
            print_colored(f"\n📊 Placing {side} market order...", Fore.YELLOW)
            print(f"Symbol: {symbol}")
            print(f"Side: {side}")
            print(f"Quantity: {quantity}")
            
            order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type='MARKET',
                quantity=quantity
            )
            
            self.logger.info(f"Market order placed: {order}")
            print_colored("✅ Market order placed successfully!", Fore.GREEN)
            self._print_order_details(order)
            return order
            
        except BinanceAPIException as e:
            self.logger.error(f"Binance API error: {e}")
            print_colored(f"❌ Binance API error: {e}", Fore.RED)
            return None
        except Exception as e:
            self.logger.error(f"Failed to place market order: {str(e)}")
            print_colored(f"❌ Failed to place market order: {str(e)}", Fore.RED)
            return None

    def place_limit_order(self, symbol, side, quantity, price):
        """Place limit order with price validation"""
        try:
            is_valid, message = self.validate_limit_price(symbol, side, price)
            if not is_valid:
                print_colored(f"❌ Price Validation Failed: {message}", Fore.RED)
                
                suggestions = self.suggest_reasonable_prices(symbol, side)
                if suggestions:
                    print_colored("\n💡 Suggested reasonable prices:", Fore.YELLOW)
                    for desc, suggested_price in suggestions.items():
                        print(f"  {desc}: ${suggested_price}")
                
                self.logger.error(f"Price validation failed: {message}")
                return None
        
            print_colored(f"\n📊 Placing {side} limit order...", Fore.YELLOW)
            print(f"Symbol: {symbol}")
            print(f"Side: {side}")
            print(f"Quantity: {quantity}")
            print(f"Price: {price}")
            
            order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type='LIMIT',
                timeInForce='GTC',
                quantity=quantity,
                price=price
            )
            
            self.logger.info(f"Limit order placed: {order}")
            print_colored("✅ Limit order placed successfully!", Fore.GREEN)
            self._print_order_details(order)
            return order
            
        except BinanceAPIException as e:
            self.logger.error(f"Binance API error: {e}")
            print_colored(f"❌ Binance API error: {e}", Fore.RED)
            return None
        except Exception as e:
            self.logger.error(f"Failed to place limit order: {str(e)}")
            print_colored(f"❌ Failed to place limit order: {str(e)}", Fore.RED)
            return None

    def get_current_price(self, symbol):
        """Get current price for symbol"""
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol.upper())
            return float(ticker['price'])
        except Exception as e:
            self.logger.error(f"Failed to get current price: {str(e)}")
            return None

    def validate_limit_price(self, symbol, side, price):
        """Validate if limit price is within Binance acceptable range"""
        try:
            current_price = self.get_current_price(symbol)
            if not current_price:
                return False, "Could not get current price"
            
            side = side.upper()
            price = float(price)
            
            
            max_deviation = 0.5  # 50%
            
            if side == 'BUY':
              
                max_allowed_price = current_price * (1 + max_deviation)
                if price > max_allowed_price:
                    return False, f"BUY price ${price} too high. Max allowed: ${max_allowed_price:.2f}"
            
            elif side == 'SELL':

                min_allowed_price = current_price * (1 - max_deviation)
                if price < min_allowed_price:
                    return False, f"SELL price ${price} too low. Min allowed: ${min_allowed_price:.2f}"
            
            return True, "Price is valid"
            
        except Exception as e:
            return False, f"Price validation error: {str(e)}"

    def suggest_reasonable_prices(self, symbol, side):
        """Suggest reasonable prices for limit orders"""
        try:
            current_price = self.get_current_price(symbol)
            if not current_price:
                return None
            
            side = side.upper()
            suggestions = {}
            
            if side == 'BUY':

                suggestions = {
                    "Aggressive (2% below)": round(current_price * 0.98, 2),
                    "Moderate (5% below)": round(current_price * 0.95, 2),
                    "Conservative (10% below)": round(current_price * 0.90, 2)
                }
            elif side == 'SELL':

                suggestions = {
                    "Aggressive (2% above)": round(current_price * 1.02, 2),
                    "Moderate (5% above)": round(current_price * 1.05, 2),
                    "Conservative (10% above)": round(current_price * 1.10, 2)
                }
            
            return suggestions
            
        except Exception as e:
            self.logger.error(f"Failed to suggest prices: {str(e)}")
            return None

    def _print_order_details(self, order):
        """Print order details in a formatted way"""
        print_colored("\n📋 Order Details:", Fore.CYAN)
        print(f"  Order ID: {order.get('orderId')}")
        print(f"  Symbol: {order.get('symbol')}")
        print(f"  Side: {order.get('side')}")
        print(f"  Type: {order.get('type')}")
        print(f"  Status: {order.get('status')}")
        print(f"  Quantity: {order.get('origQty')}")
        if order.get('price'):
            print(f"  Price: {order.get('price')}")