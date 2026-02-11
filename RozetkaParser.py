from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import time


def get_rozetka_price(url):
    options = Options()
    # Убираем флаг автоматизации
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Рекомендую добавить headless режим, если не нужно смотреть на окно браузера
    # options.add_argument('--headless=new')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print(f"Загружаем страницу: {url}")
        driver.get(url)

        # Ждем появления цены (используем более универсальный класс)
        # На Розетке цена обычно лежит в p.product-price__big или подобных
        wait = WebDriverWait(driver, 15)

        # 1. Ждем элемент. Используем класс, который редко меняется для больших цен.
        price_element = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "product-price__big")
        ))

        # 2. Получаем текст
        price_text = price_element.text
        print(f"Найденный текст цены: {price_text}")

        # 3. Очистка от лишних символов (пробелы, валюта)
        # Розетка часто использует неразрывные пробелы, поэтому re.sub — это правильный выбор
        price = re.sub(r'[^\d]', '', price_text)

        return int(price)

    except Exception as e:
        print(f"Ошибка при парсинге: {e}")
        driver.save_screenshot("debug_screen.png")
        return None

    finally:
        driver.quit()


# Тест
if __name__ == "__main__":
    url = "https://rozetka.com.ua/ua/apple-airpods-pro-3-with-magsafe-case-usb-c-mfhp4ze-a/p543663795/"
    price = get_rozetka_price(url)

    if price:
        print(f"\n✅ Успех! Цена: {price} грн")
    else:
        print("\n❌ Не удалось получить цену. Проверь файл debug_screen.png")