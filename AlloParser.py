from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import re


def get_allo_price(url):
    """
    Extract price from Allo.ua product page
    
    Args:
        url (str): Product page URL
        
    Returns:
        int: Price in UAH or None if not found
    """
    options = Options()
    # Remove automation flags
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # Uncomment for headless mode
    # options.add_argument('--headless=new')
    
    try:
        # Use standard ChromeDriver with webdriver-manager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        print(f"Opening page: {url}")
        driver.get(url)
        
        # Wait for page to load (Allo may have anti-bot protection)
        time.sleep(10)
        
        # Method 1: Try to find price in JSON-LD structured data (disabled for now)
        # scripts = driver.find_elements(By.XPATH, "//script[@type='application/ld+json']")
        # print(f"Found {len(scripts)} JSON-LD scripts")
        # for i, script in enumerate(scripts):
        #     try:
        #         data = json.loads(script.get_attribute('innerHTML'))
        #         items = data if isinstance(data, list) else [data]
        #         for item in items:
        #             if 'offers' in item:
        #                 price = item['offers'].get('price')
        #                 print(f"JSON-LD method found price: {price}")
        #                 if price:
        #                     price_int = int(float(price))
        #                     print(f"Returning JSON-LD price: {price_int}")
        #                     return price_int
        #     except Exception as e:
        #         print(f"Error parsing JSON-LD script {i}: {e}")
        #         continue
        
        # Method 2: Try common price selectors used by Allo
        price_selectors = [
            ".a-product-price__current-price",
            ".product-price__big",
            ".price__current",
            ".product-price__current",
            ".price-value",
            "[data-testid='price']",
            ".price",
            ".product-price"
        ]
        
        wait = WebDriverWait(driver, 10)
        
        # First, let's try to find the specific class mentioned by the user
        try:
            specific_element = driver.find_element(By.CLASS_NAME, "a-product-price__current-price")
            # Get the raw text and handle encoding issues
            specific_text = specific_element.get_attribute('textContent') or specific_element.text
            # Remove all whitespace and non-digit characters
            price = re.sub(r'[^\d]', '', specific_text)
            if price and len(price) > 2:
                return int(price)
        except:
            pass
        
        for selector in price_selectors:
            try:
                price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                price_text = price_element.get_attribute('textContent') or price_element.text
                price_text = price_text.strip()
                
                # Skip empty price texts
                if not price_text:
                    continue
                
                # Clean price text - remove all non-digit characters
                price = re.sub(r'[^\d]', '', price_text)
                
                if price and len(price) > 2:  # Ensure we have a meaningful price (at least 3 digits)
                    return int(price)
            except:
                continue
        
        # Method 3: Look for any element containing price-like numbers
        try:
            # Search for elements that look like prices (UAH prices typically have 3-6 digits)
            price_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'грн')]")
            for element in price_elements:
                text = element.get_attribute('textContent') or element.text
                price_match = re.search(r'(\d{3,6})\s*(?:грн)', text)
                if price_match:
                    return int(price_match.group(1))
        except:
            pass
        
        print("Price not found with any method")
        return None
        
    except Exception as e:
        print(f"Error occurred: {e}")
        # Save screenshot for debugging
        try:
            driver.save_screenshot("allo_debug.png")
            print("Debug screenshot saved as allo_debug.png")
        except:
            pass
        return None
    finally:
        try:
            driver.quit()
        except:
            pass


if __name__ == "__main__":
    # Test with a sample Allo product URL
    test_urls = [
        "https://allo.ua/ua/naushniki/naushniki-apple-airpods-pro-2nd-gen-usb-c-mtjv3ty-a-white.html",
        "https://allo.ua/ua/products/mobile/apple-iphone-15-pro-max-256gb-titanium-naturalnyj.html"
    ]
    
    for url in test_urls:
        print(f"\n=== Testing URL: {url} ===")
        price = get_allo_price(url)
        
        if price:
            print(f"Success! Price: {price} UAH")
        else:
            print("Failed to get price")
        
        print("=" * 50)
