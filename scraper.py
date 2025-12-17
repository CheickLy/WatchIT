import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time
import os
import random


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class RealTimeTrendTracker:
    def __init__(self, url, product_name, use_selenium=False):
        self.url = url
        self.product_name = product_name
        self.use_selenium = use_selenium
        self.storage_file = "tracker_data.csv"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

    def fetch_price_bs4(self):
        """Fast scraping for simple sites."""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Selector for 'Books to Scrape'
            price_elem = soup.select_one(".price_color")
            if price_elem:
                return float(price_elem.get_text().replace('£', '').replace('$', ''))
            return None
        except Exception as e:
            print(f"BS4 Error: {e}")
            return None

    def fetch_price_selenium(self):
        """Advanced scraping for Nike and JavaScript-heavy sites."""
        options = Options()
        options.add_argument("--headless")  
        options.add_argument("--disable-gpu")
        options.add_argument(f"user-agent={self.headers['User-Agent']}")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        try:
            driver.get(self.url)
            # Wait up to 15 seconds for the Nike price class to appear
            wait = WebDriverWait(driver, 15)
            
            # This selector covers the Nike price class you provided
            selector = "div[data-test='product-price'], .product-price, .css-tbgmka"
            price_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            
            price_text = price_elem.text
            # Clean up: '£124.95' -> 124.95
            price = float(''.join(c for c in price_text if c.isdigit() or c == '.'))
            return price
        except Exception as e:
            print(f"Selenium Error: {e}")
            return None
        finally:
            driver.quit()

    def save_data(self, price):
        timestamp = datetime.now().strftime("%H:%M:%S")
        new_data = pd.DataFrame([[timestamp, price]], columns=["Timestamp", "Price"])
        file_exists = os.path.isfile(self.storage_file) and os.path.getsize(self.storage_file) > 0
        new_data.to_csv(self.storage_file, mode='a' if file_exists else 'w', 
                        header=not file_exists, index=False)

    def visualize(self):
        if not os.path.isfile(self.storage_file): return
        df = pd.read_csv(self.storage_file)
        plt.figure(figsize=(10, 5))
        plt.plot(df['Timestamp'], df['Price'], marker='o', color='tab:orange')
        plt.title(f"Trend: {self.product_name}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def run(self, iterations=5, interval=10):
        print(f"Tracking {self.product_name} using {'Selenium' if self.use_selenium else 'BS4'}...")
        try:
            for _ in range(iterations):
                price = self.fetch_price_selenium() if self.use_selenium else self.fetch_price_bs4()
                if price:
                    print(f"Saved Price: £{price}")
                    self.save_data(price)
                time.sleep(interval)
        except KeyboardInterrupt:
            pass
        self.visualize()

if __name__ == "__main__":
    # TEST 1: Simple Site (BS4)
    # tracker = RealTimeTrendTracker("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html", "Book")
    
    # TEST 2: Complex Site (Nike)
    NIKE_URL = "https://www.nike.com/t/air-jordan-4-rm-mens-shoes-Q1Cbd2ry/HF8126-100"
    tracker = RealTimeTrendTracker(NIKE_URL, "AIR JORDAN 4 RM", use_selenium=True)
    
    tracker.run(iterations=3, interval=5)