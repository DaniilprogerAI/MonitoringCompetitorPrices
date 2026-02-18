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


def get_foxtrot_price_fixed(url):
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

        # Wait for page to load (Cloudflare may take time)
        time.sleep(7)

        # Look for price in JSON-LD structured data
        scripts = driver.find_elements(By.XPATH, "//script[@type='application/ld+json']")
        for script in scripts:
            try:
                data = json.loads(script.get_attribute('innerHTML'))
                items = data if isinstance(data, list) else [data]
                for item in items:
                    if 'offers' in item:
                        price = item['offers'].get('price')
                        if price:
                            return int(float(price))
            except:
                continue

        return None

    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    # Тест
    url = "https://www.foxtrot.com.ua/uk/shop/naushniki-apple-airpods-3-pro.html"
    price = get_foxtrot_price_fixed(url)
    print(f"💰 Результат: {price} грн" if price else "❌ Цена не найдена")