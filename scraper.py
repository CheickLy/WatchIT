import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time
import os

class TrendTracker:
    def __init__(self, url, product_name, storage_file="tracker_data.csv"):
        self.url = url
        self.product_name = product_name
        self.storage_file = storage_file
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def fetch_price(self):
        """Extracts price from target URL."""
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
    
            price_text = soup.select_one(".a-price-whole").get_text()
            price = float(price_text.replace(',', '').replace('$', ''))
            return price
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None