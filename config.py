import os

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID_HERE')

# Monitoring Configuration
CHECK_INTERVAL_HOURS = 2  # Check every 2 hours
PRICE_DROP_THRESHOLD = 5.0  # Alert on price drop > 5%

# CSV File Configuration
HISTORY_FILE = 'price_history.csv'

# Competitor Parsers
PARSERS = {
    'rozetka': 'RozetkaParser',
    'foxtrot': 'FoxtrotParser', 
    'allo': 'AlloParser'
}
