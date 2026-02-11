import undetected_chromedriver as uc
import time
import json
import re


def get_foxtrot_price_fixed(url):
    options = uc.ChromeOptions()
    # На всякий случай добавим headless, если не хочешь видеть окно
    # options.add_argument('--headless')

    try:
        # Явно указываем версию 144, чтобы он не искал 145-ю
        driver = uc.Chrome(options=options, version_main=144)

        print(f"Открываем страницу: {url}")
        driver.get(url)

        # Ждем прогрузки (Cloudflare может занять время)
        time.sleep(7)

        # Ищем цену в JSON-LD (самый надежный метод)
        scripts = driver.find_elements(uc.By.XPATH, "//script[@type='application/ld+json']")
        for script in scripts:
            try:
                data = json.loads(script.get_attribute('innerHTML'))
                items = data if isinstance(data, list) else [data]
                for item in items:
                    # Ищем поле price в структуре Product или Offers
                    if 'offers' in item:
                        price = item['offers'].get('price')
                        if price:
                            return int(float(price))
            except:
                continue

        return None

    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
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