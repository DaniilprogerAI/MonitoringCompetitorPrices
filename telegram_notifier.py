import requests
import logging
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class TelegramNotifier:
    def __init__(self, bot_token=None, chat_id=None):
        self.bot_token = bot_token or TELEGRAM_BOT_TOKEN
        self.chat_id = chat_id or TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
    def send_message(self, message):
        """Send message to Telegram chat"""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            
            logging.info(f"Telegram message sent successfully")
            return True
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send Telegram message: {e}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error sending Telegram message: {e}")
            return False
    
    def send_price_drop_alert(self, product_name, competitor, old_price, new_price, our_price):
        """Send formatted price drop alert"""
        price_drop = old_price - new_price
        drop_percentage = (price_drop / old_price) * 100
        
        message = f"""
🚨 <b>PRICE DROP ALERT</b> 🚨

<b>Product:</b> {product_name}
<b>Competitor:</b> {competitor.capitalize()}
<b>Price Drop:</b> {price_drop} UAH (-{drop_percentage:.1f}%)

<b>Old Price:</b> {old_price:,} UAH
<b>New Price:</b> {new_price:,} UAH
<b>Our Price:</b> {our_price:,} UAH

💡 <b>Recommendation:</b> Reduce our price to {new_price:,} UAH to match competitor
        """
        
        return self.send_message(message)
    
    def test_connection(self):
        """Test Telegram bot connection"""
        message = "✅ TechnoSmart Price Monitor is now active!"
        return self.send_message(message)
