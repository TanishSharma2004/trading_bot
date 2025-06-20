#!/usr/bin/env python3
"""
Binance Futures Trading Bot
A simple command-line trading bot for Binance Futures Testnet
"""

import sys
from bot import BasicBot
from utils import print_colored, validate_symbol, validate_quantity
from colorama import Fore, Style

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════╗
    ║        BINANCE TRADING BOT           ║
    ║            Testnet Mode              ║
    ╚══════════════════════════════════════╝
    """
    print_colored(banner, Fore.CYAN)

def print_menu():
    """Print main menu"""
    menu = """
    🔹 Available Commands:
    1. test      - Test API connection
    2. balance   - Show account balance
    3. price     - Get current price for symbol
    4. limits    - Show price limits for symbol
    5. market    - Place market order
    6. limit     - Place limit order
    7. help      - Show this menu
    8. quit      - Exit the bot
    """
    print_colored(menu, Fore.YELLOW)

def get_user_input(prompt, input_type=str, validator=None):
    """Get and validate user input"""
    while True:
        try:
            user_input = input(f"{prompt}: ").strip()
            if user_input.lower() == 'quit':
                return None
            
            converted_input = input_type(user_input)
            
            if validator and not validator(converted_input):
                print_colored("❌ Invalid input. Please try again.", Fore.RED)
                continue
                
            return converted_input
        except ValueError:
            print_colored("❌ Invalid input type. Please try again.", Fore.RED)
        except KeyboardInterrupt:
            return None

def handle_market_order(bot):
    """Handle market order placement"""
    print_colored("\n📊 Market Order", Fore.CYAN)
    
    symbol = get_user_input("Enter symbol (e.g., BTCUSDT)", str, validate_symbol)
    if not symbol:
        return
    
    side = get_user_input("Enter side (BUY/SELL)", str, lambda x: x.upper() in ['BUY', 'SELL'])
    if not side:
        return
    
    quantity = get_user_input("Enter quantity", float, validate_quantity)
    if not quantity:
        return
    
    bot.place_market_order(symbol, side, quantity)

def handle_limit_order(bot):
    """Handle limit order placement with price suggestions"""
    print_colored("\n📊 Limit Order", Fore.CYAN)
    
    symbol = get_user_input("Enter symbol (e.g., BTCUSDT)", str, validate_symbol)
    if not symbol:
        return
    
    # Show current price
    current_price = bot.get_current_price(symbol)
    if current_price:
        print_colored(f"💰 Current price: ${current_price}", Fore.GREEN)
    else:
        print_colored("❌ Could not get current price", Fore.RED)
        return
    
    side = get_user_input("Enter side (BUY/SELL)", str, lambda x: x.upper() in ['BUY', 'SELL'])
    if not side:
        return
    
    # Show price suggestions
    suggestions = bot.suggest_reasonable_prices(symbol, side)
    if suggestions:
        print_colored(f"\n💡 Suggested {side.upper()} prices:", Fore.YELLOW)
        for desc, suggested_price in suggestions.items():
            print(f"  {desc}: ${suggested_price}")
        print()
    
    quantity = get_user_input("Enter quantity", float, validate_quantity)
    if not quantity:
        return
    
    price_prompt = f"Enter price (Current: ${current_price})"
    price = get_user_input(price_prompt, float, lambda x: x > 0)
    if not price:
        return
    
    bot.place_limit_order(symbol, side, quantity, price)

def handle_price_limits(bot):
    """Show price limits for a symbol"""
    symbol = get_user_input("Enter symbol (e.g., BTCUSDT)", str, validate_symbol)
    if not symbol:
        return
    
    current_price = bot.get_current_price(symbol)
    if not current_price:
        print_colored("❌ Could not get current price", Fore.RED)
        return
    
    print_colored(f"\n📊 Price Limits for {symbol}:", Fore.CYAN)
    print(f"Current Price: ${current_price}")
    
    max_buy_price = current_price * 1.5
    min_sell_price = current_price * 0.5
    
    print_colored("\n🔹 BUY Order Limits:", Fore.YELLOW)
    print(f"  Maximum BUY price: ${max_buy_price:.2f}")
    print(f"  Reasonable range: ${current_price * 0.95:.2f} - ${current_price * 1.05:.2f}")
    
    print_colored("\n🔹 SELL Order Limits:", Fore.YELLOW)
    print(f"  Minimum SELL price: ${min_sell_price:.2f}")
    print(f"  Reasonable range: ${current_price * 1.05:.2f} - ${current_price * 1.15:.2f}")
    
    print_colored("\n💡 Tips:", Fore.GREEN)
    print("  • BUY below current price to get a good deal")
    print("  • SELL above current price to make profit")
    print("  • Stay within 10% of current price for better execution")

def handle_price_check(bot):
    """Handle price checking"""
    symbol = get_user_input("Enter symbol (e.g., BTCUSDT)", str, validate_symbol)
    if not symbol:
        return
    
    price = bot.get_current_price(symbol)
    if price:
        print_colored(f"💰 {symbol} current price: ${price}", Fore.GREEN)

def main():
    """Main application loop"""
    print_banner()
    
    try:
        # Initialize bot
        bot = BasicBot()
        
        # Test connection
        if not bot.test_connection():
            print_colored("❌ Cannot connect to Binance API. Please check your credentials.", Fore.RED)
            sys.exit(1)
        
        print_menu()
        
        while True:
            try:
                command = input(f"\n{Fore.CYAN}Enter command (help for menu): {Style.RESET_ALL}").strip().lower()
                
                if command in ['quit', 'exit', 'q']:
                    print_colored("👋 Goodbye!", Fore.CYAN)
                    break
                
                elif command == 'help':
                    print_menu()
                
                elif command == 'test':
                    bot.test_connection()
                
                elif command == 'balance':
                    bot.get_account_balance()
                
                elif command == 'price':
                    handle_price_check(bot)
                
                elif command == 'market':
                    handle_market_order(bot)
                
                elif command == 'limit':
                    handle_limit_order(bot)
                
                elif command == 'limits':
                    handle_price_limits(bot)
                
                else:
                    print_colored("❌ Unknown command. Type 'help' for available commands.", Fore.RED)
                       
            except KeyboardInterrupt:
                print_colored("\n👋 Goodbye!", Fore.CYAN)
                break
            except Exception as e:
                print_colored(f"❌ An error occurred: {str(e)}", Fore.RED)
    
    except Exception as e:
        print_colored(f"❌ Failed to initialize bot: {str(e)}", Fore.RED)
        sys.exit(1)

if __name__ == "__main__":
    main()