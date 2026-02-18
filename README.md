# TechnoSmart Price Monitoring System

Automatic price monitoring system for TechnoSmart electronics store that tracks competitor prices and sends alerts via Telegram when significant price drops are detected.

## Features

- **Multi-competitor monitoring**: Tracks prices from Rozetka, Foxtrot, and Allo
- **Real-time alerts**: Sends Telegram notifications when competitors drop prices by >5%
- **Historical data**: Stores all price checks in CSV format
- **Automated scheduling**: Runs every 2 hours automatically
- **Robust parsing**: Uses specialized parsers for each competitor website

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Telegram bot:
   - Create a bot via [@BotFather](https://t.me/botfather) on Telegram
   - Get your bot token and chat ID
   - Set environment variables:
     ```bash
     set TELEGRAM_BOT_TOKEN=your_bot_token_here
     set TELEGRAM_CHAT_ID=your_chat_id_here
     ```
   - Or update `config.py` directly

3. Configure products in `products.json`:
   - Add your products with TechnoSmart prices and competitor URLs
   - Update margins as needed

## Usage

### Production Mode
```bash
python main.py
```
Starts the automated monitoring system that runs every 2 hours.

### Test Mode
```bash
python main.py --test
```
Runs monitoring once and exits (useful for testing).

### Create Mock Data
```bash
python main.py --mock
```
Creates sample historical data for testing the alert system.

## Configuration

### `products.json`
Define products to monitor:
```json
{
  "products": [
    {
      "name": "Product Name",
      "technosmart_price": 9999,
      "margin": 15,
      "urls": {
        "rozetka": "https://rozetka.com.ua/...",
        "foxtrot": "https://www.foxtrot.com.ua/...",
        "allo": "https://allo.ua/..."
      }
    }
  ]
}
```

### `config.py`
Key settings:
- `CHECK_INTERVAL_HOURS`: Monitoring frequency (default: 2 hours)
- `PRICE_DROP_THRESHOLD`: Alert trigger percentage (default: 5%)
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `TELEGRAM_CHAT_ID`: Target chat ID for notifications

## Alert Format

When a price drop >5% is detected, the system sends:

```
🚨 PRICE DROP ALERT 🚨

Product: Samsung Galaxy Buds2 Pro
Competitor: Rozetka
Price Drop: 300 UAH (-5.3%)

Old Price: 5,699 UAH
New Price: 5,399 UAH
Our Price: 5,499 UAH

💡 Recommendation: Reduce our price to 5,399 UAH to match competitor
```

## File Structure

```
MonitoringCompetitorPrices/
├── main.py              # Main monitoring script
├── config.py            # Configuration settings
├── products.json         # Product definitions
├── telegram_notifier.py  # Telegram notification system
├── price_history.py     # CSV history management
├── RozetkaParser.py     # Rozetka price parser
├── FoxtrotParser.py     # Foxtrot price parser
├── AlloParser.py        # Allo price parser
├── requirements.txt      # Python dependencies
├── price_history.csv    # Historical price data
└── price_monitor.log    # Application logs
```

## Testing

The system includes mock data for testing scenarios:
- Samsung Galaxy Buds2 Pro price drop from 5,699 to 5,399 UAH (-5.3%) on Jan 30
- This should trigger an alert when the system detects the change

## Monitoring Process

1. **Data Collection**: Every 2 hours, the system visits each competitor's product page
2. **Price Extraction**: Uses specialized parsers to extract current prices
3. **Change Analysis**: Compares new prices with previously recorded data
4. **Alert Generation**: Sends Telegram notifications for price drops >5%
5. **History Storage**: Saves all price data to CSV for analysis

## Troubleshooting

- **Parser failures**: Check `price_monitor.log` for detailed error messages
- **Telegram issues**: Verify bot token and chat ID in configuration
- **Missing prices**: Some products may be out of stock or temporarily unavailable
- **Rate limiting**: The system includes delays between requests to avoid blocking

## Dependencies

- **selenium**: Web browser automation for price extraction
- **pandas**: Data manipulation and CSV handling
- **requests**: HTTP requests for Telegram API
- **schedule**: Task scheduling for automated monitoring
- **webdriver-manager**: Automatic ChromeDriver management
