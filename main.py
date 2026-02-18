import json
import logging
import time
import schedule
from datetime import datetime
from typing import Dict, Optional

from config import PARSERS, CHECK_INTERVAL_HOURS, PRICE_DROP_THRESHOLD
from telegram_notifier import TelegramNotifier
from price_history import PriceHistory

# Import parser modules
import RozetkaParser
import FoxtrotParser
import AlloParser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('price_monitor.log'),
        logging.StreamHandler()
    ]
)

class PriceMonitor:
    def __init__(self):
        self.notifier = TelegramNotifier()
        self.history = PriceHistory()
        self.products = self.load_products()
        self.parser_functions = {
            'rozetka': RozetkaParser.get_rozetka_price,
            'foxtrot': FoxtrotParser.get_foxtrot_price_fixed,
            'allo': AlloParser.get_allo_price
        }
    
    def load_products(self):
        """Load products from JSON configuration file"""
        try:
            with open('products.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data['products']
        except Exception as e:
            logging.error(f"Failed to load products: {e}")
            return []
    
    def get_competitor_prices(self, product_urls: Dict[str, str]) -> Dict[str, Optional[int]]:
        """Get current prices from all competitors for a product"""
        prices = {}
        
        for competitor, url in product_urls.items():
            try:
                logging.info(f"Checking {competitor} price for {url}")
                price = self.parser_functions[competitor](url)
                prices[competitor] = price
                
                if price:
                    logging.info(f"{competitor.capitalize()} price: {price:,} UAH")
                else:
                    logging.warning(f"Failed to get {competitor} price")
                    
                # Add delay between requests to avoid being blocked
                time.sleep(2)
                
            except Exception as e:
                logging.error(f"Error getting {competitor} price: {e}")
                prices[competitor] = None
        
        return prices
    
    def check_price_drops(self, product_name: str, competitor_prices: Dict[str, Optional[int]], our_price: int):
        """Check for price drops and send alerts if necessary"""
        alerts_sent = 0
        
        for competitor, new_price in competitor_prices.items():
            if not new_price:
                continue
            
            # Get last recorded price for this competitor
            old_price = self.history.get_last_price(product_name, competitor)
            
            if old_price and new_price < old_price:
                # Calculate price drop percentage
                price_drop = old_price - new_price
                drop_percentage = (price_drop / old_price) * 100
                
                if drop_percentage > PRICE_DROP_THRESHOLD:
                    logging.info(f"PRICE DROP ALERT: {competitor} {product_name} {old_price}->{new_price} (-{drop_percentage:.1f}%)")
                    
                    # Send Telegram notification
                    success = self.notifier.send_price_drop_alert(
                        product_name=product_name,
                        competitor=competitor,
                        old_price=old_price,
                        new_price=new_price,
                        our_price=our_price
                    )
                    
                    if success:
                        alerts_sent += 1
                        logging.info(f"Alert sent for {competitor} {product_name}")
                    else:
                        logging.error(f"Failed to send alert for {competitor} {product_name}")
        
        return alerts_sent
    
    def monitor_all_products(self):
        """Monitor all products for price changes"""
        logging.info("Starting price monitoring cycle")
        
        total_products = len(self.products)
        successful_checks = 0
        alerts_sent = 0
        
        for product in self.products:
            try:
                product_name = product['name']
                our_price = product['technosmart_price']
                urls = product['urls']
                
                logging.info(f"Monitoring product: {product_name}")
                
                # Get current competitor prices
                competitor_prices = self.get_competitor_prices(urls)
                
                # Check for price drops and send alerts
                alerts_sent += self.check_price_drops(product_name, competitor_prices, our_price)
                
                # Save to history
                self.history.add_price_record(product_name, our_price, competitor_prices)
                
                successful_checks += 1
                
            except Exception as e:
                logging.error(f"Error monitoring product {product.get('name', 'Unknown')}: {e}")
        
        logging.info(f"Monitoring cycle completed: {successful_checks}/{total_products} products checked, {alerts_sent} alerts sent")
    
    def run_once(self):
        """Run monitoring once (for testing)"""
        self.monitor_all_products()
    
    def start_scheduler(self):
        """Start the scheduled monitoring"""
        logging.info(f"Starting price monitor with {CHECK_INTERVAL_HOURS}-hour intervals")
        
        # Schedule monitoring to run every specified hours
        schedule.every(CHECK_INTERVAL_HOURS).hours.do(self.monitor_all_products)
        
        # Test Telegram connection on startup
        if self.notifier.test_connection():
            logging.info("Telegram connection test successful")
        else:
            logging.error("Telegram connection test failed")
        
        # Run once immediately on startup
        self.monitor_all_products()
        
        # Keep the scheduler running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute if scheduled task is due

def main():
    """Main entry point"""
    import sys
    
    monitor = PriceMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Test mode - run once and exit
        logging.info("Running in test mode")
        monitor.run_once()
    elif len(sys.argv) > 1 and sys.argv[1] == '--mock':
        # Create mock data for testing
        logging.info("Creating mock data")
        monitor.history.create_mock_data()
        logging.info("Mock data created successfully")
    else:
        # Production mode - start scheduler
        try:
            monitor.start_scheduler()
        except KeyboardInterrupt:
            logging.info("Price monitor stopped by user")
        except Exception as e:
            logging.error(f"Price monitor crashed: {e}")
            raise

if __name__ == "__main__":
    main()