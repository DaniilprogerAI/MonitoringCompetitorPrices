import pandas as pd
import os
from datetime import datetime
from config import HISTORY_FILE
import logging

class PriceHistory:
    def __init__(self, history_file=None):
        self.history_file = history_file or HISTORY_FILE
        self.ensure_history_file()
    
    def ensure_history_file(self):
        """Create CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.history_file):
            df = pd.DataFrame(columns=[
                'date', 'product', 'technosmart_price', 
                'rozetka_price', 'foxtrot_price', 'allo_price'
            ])
            df.to_csv(self.history_file, index=False)
            logging.info(f"Created new history file: {self.history_file}")
    
    def add_price_record(self, product_name, technosmart_price, competitor_prices):
        """Add new price record to history"""
        try:
            # Read existing data
            df = pd.read_csv(self.history_file)
            
            # Create new record
            new_record = {
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'product': product_name,
                'technosmart_price': technosmart_price,
                'rozetka_price': competitor_prices.get('rozetka'),
                'foxtrot_price': competitor_prices.get('foxtrot'),
                'allo_price': competitor_prices.get('allo')
            }
            
            # Append new record
            df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
            
            # Save back to CSV
            df.to_csv(self.history_file, index=False)
            
            logging.info(f"Added price record for {product_name}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to add price record: {e}")
            return False
    
    def get_last_price(self, product_name, competitor):
        """Get the last recorded price for a specific product and competitor"""
        try:
            df = pd.read_csv(self.history_file)
            
            # Filter for specific product and competitor
            product_data = df[df['product'] == product_name].copy()
            
            if product_data.empty:
                return None
            
            # Get the most recent record
            latest_record = product_data.iloc[-1]
            price_column = f'{competitor}_price'
            
            return latest_record[price_column] if pd.notna(latest_record[price_column]) else None
            
        except Exception as e:
            logging.error(f"Failed to get last price: {e}")
            return None
    
    def get_price_history(self, product_name, days=7):
        """Get price history for a product for the last N days"""
        try:
            df = pd.read_csv(self.history_file)
            
            # Convert date column to datetime
            df['date'] = pd.to_datetime(df['date'])
            
            # Filter for specific product and date range
            cutoff_date = datetime.now() - pd.Timedelta(days=days)
            product_data = df[
                (df['product'] == product_name) & 
                (df['date'] >= cutoff_date)
            ].sort_values('date')
            
            return product_data
            
        except Exception as e:
            logging.error(f"Failed to get price history: {e}")
            return pd.DataFrame()
    
    def create_mock_data(self):
        """Create mock data for testing based on requirements"""
        mock_data = [
            # Samsung Galaxy Buds2 Pro - price drop on Jan 30
            {'date': '2026-01-28 10:00:00', 'product': 'Samsung Galaxy Buds2 Pro', 'technosmart_price': 5499, 'rozetka_price': 5699, 'foxtrot_price': 5799, 'allo_price': 5899},
            {'date': '2026-01-29 10:00:00', 'product': 'Samsung Galaxy Buds2 Pro', 'technosmart_price': 5499, 'rozetka_price': 5699, 'foxtrot_price': 5799, 'allo_price': 5899},
            {'date': '2026-01-30 10:00:00', 'product': 'Samsung Galaxy Buds2 Pro', 'technosmart_price': 5499, 'rozetka_price': 5399, 'foxtrot_price': 5799, 'allo_price': 5899},  # Price drop: 5699->5399 (-5.3%)
            {'date': '2026-01-31 10:00:00', 'product': 'Samsung Galaxy Buds2 Pro', 'technosmart_price': 5499, 'rozetka_price': 5399, 'foxtrot_price': 5799, 'allo_price': 5899},
            {'date': '2026-02-01 10:00:00', 'product': 'Samsung Galaxy Buds2 Pro', 'technosmart_price': 5499, 'rozetka_price': 5399, 'foxtrot_price': 5799, 'allo_price': 5899},
            {'date': '2026-02-02 10:00:00', 'product': 'Samsung Galaxy Buds2 Pro', 'technosmart_price': 5499, 'rozetka_price': 5399, 'foxtrot_price': 5799, 'allo_price': 5899},
            {'date': '2026-02-03 10:00:00', 'product': 'Samsung Galaxy Buds2 Pro', 'technosmart_price': 5499, 'rozetka_price': 5399, 'foxtrot_price': 5799, 'allo_price': 5899},
            
            # Apple AirPods Pro - stable prices
            {'date': '2026-01-28 10:00:00', 'product': 'Apple AirPods Pro', 'technosmart_price': 28999, 'rozetka_price': 29999, 'foxtrot_price': 30999, 'allo_price': 31999},
            {'date': '2026-01-29 10:00:00', 'product': 'Apple AirPods Pro', 'technosmart_price': 28999, 'rozetka_price': 29999, 'foxtrot_price': 30999, 'allo_price': 31999},
            {'date': '2026-01-30 10:00:00', 'product': 'Apple AirPods Pro', 'technosmart_price': 28999, 'rozetka_price': 29999, 'foxtrot_price': 30999, 'allo_price': 31999},
            {'date': '2026-01-31 10:00:00', 'product': 'Apple AirPods Pro', 'technosmart_price': 28999, 'rozetka_price': 29999, 'foxtrot_price': 30999, 'allo_price': 31999},
            {'date': '2026-02-01 10:00:00', 'product': 'Apple AirPods Pro', 'technosmart_price': 28999, 'rozetka_price': 29999, 'foxtrot_price': 30999, 'allo_price': 31999},
            {'date': '2026-02-02 10:00:00', 'product': 'Apple AirPods Pro', 'technosmart_price': 28999, 'rozetka_price': 29999, 'foxtrot_price': 30999, 'allo_price': 31999},
            {'date': '2026-02-03 10:00:00', 'product': 'Apple AirPods Pro', 'technosmart_price': 28999, 'rozetka_price': 29999, 'foxtrot_price': 30999, 'allo_price': 31999},
        ]
        
        df = pd.DataFrame(mock_data)
        df.to_csv(self.history_file, index=False)
        logging.info(f"Created mock data with {len(mock_data)} records")
