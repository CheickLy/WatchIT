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
        # This is the "attribute" that was missing:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_price(self):
        """Extracts price from the target URL."""
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Selector for toscrape.com
            price_element = soup.select_one(".price_color")
            
            if price_element:
                price_text = price_element.get_text()
                # Removes currency symbols
                price = float(price_text.replace('£', '').replace('$', ''))
                return price
            return None
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def save_data(self, price):
        """Appends new price data to a CSV file with strict header management."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        new_data = pd.DataFrame([[timestamp, price]], columns=["Timestamp", "Price"])
        
        # Check if file exists AND is not empty
        file_exists = os.path.isfile(self.storage_file) and os.path.getsize(self.storage_file) > 0
        
        if not file_exists:
            # Create the file with headers
            new_data.to_csv(self.storage_file, index=False)
        else:
            # Append without writing the header again
            new_data.to_csv(self.storage_file, mode='a', header=False, index=False)

    def check_for_alerts(self, current_price):
        """Detects price changes based on the last entry in CSV."""
        # Only check if file exists AND is not empty
        if os.path.isfile(self.storage_file) and os.path.getsize(self.storage_file) > 0:
            try:
                df = pd.read_csv(self.storage_file)
                if not df.empty:
                    previous_price = df.iloc[-1]['Price']
                    if current_price < previous_price:
                        print(f"🚨 ALERT: Price dropped to £{current_price}!")
                    elif current_price > previous_price:
                        print(f"📈 Trend: Price increased to £{current_price}.")
                    else:
                        print("➖ No change in price.")
            except Exception:
                # If the file is corrupted or unreadable, just skip the alert
                pass

    def visualize_trends(self):
        """Generates a line chart of the price history."""
        if not os.path.isfile(self.storage_file):
            print("No data file found to visualize.")
            return
            
        df = pd.read_csv(self.storage_file)
        
        # Debugging: Print columns to console if it fails again
        if 'Timestamp' not in df.columns or 'Price' not in df.columns:
            print(f"Error: Found columns {df.columns.tolist()}, expected ['Timestamp', 'Price']")
            return

        print("Generating graph...")
        plt.figure(figsize=(10, 6))
        plt.plot(df['Timestamp'], df['Price'], marker='o', linestyle='-', color='red')
        plt.title(f"Price Trend: {self.product_name}")
        plt.xlabel("Time")
        plt.ylabel("Price (£)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show() # This opens the window

    def run(self, interval_seconds=10):
        print(f"Starting tracker for: {self.product_name}...")
        try:
            while True:
                price = self.fetch_price()
                if price is not None:
                    # --- SWAPPED THESE TWO ---
                    self.save_data(price) # Save first so file isn't empty
                    self.check_for_alerts(price) 
                    # -------------------------
                    print(f"Saved entry: £{price}")
                
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\nStopping...")
            self.visualize_trends()

if __name__ == "__main__":
    URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html" 
    tracker = TrendTracker(URL, "A Light in the Attic")
    tracker.run(interval_seconds=10)