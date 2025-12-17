
# WatchIT (Hybrid Web Scraper)

A sophisticated Python-based data extraction tool designed to track price trends across different web architectures. This project demonstrates the ability to handle both static HTML and dynamic, JavaScript-heavy websites using a hybrid scraping approach.

## 🚀 Features
- **Hybrid Extraction Engine**: Switches between `BeautifulSoup4` (for speed/efficiency) and `Selenium` (for dynamic JavaScript rendering).
- **Anti-Bot Navigation**: Implements custom headers and headless browser configurations to navigate enterprise-level sites like Nike.
- **Data Persistence**: Automates data logging to CSV with strict error handling for data integrity.
- **Trend Visualization**: Generates real-time time-series plots using `Matplotlib` to visualize price fluctuations.
- **Alert System**: Detects and logs price changes (drops or increases) between consecutive scrapes.

  


🔍 Scraping Strategy & Design Decisions
## The "Empty soup Problem"

Some modern websites (e.g., Nike) are built as Single Page Applications (SPAs), where content is rendered dynamically via JavaScript rather than delivered as static HTML.

For these sites, traditional tools like requests and BeautifulSoup may not reliably extract data because the HTML content is loaded after the initial page request. In such cases, browser automation tools like Selenium are more appropriate, as they allow JavaScript to fully execute before scraping. Beautiful soups reads the javascript as a "blank sheet" making it unable to scrape the information needed from said sites.

Additionally, large companies often use bot-detection services (e.g., Cloudflare) and frequently changing CSS class names. To improve scraping stability, this project prioritizes HTML data attributes and other consistent selectors when available, rather than relying on brittle CSS class names.

This approach improves maintainability and reduces breakage when site layouts change.

EXAMPLE of BeautifulSoup use website (STATIC)
URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html" 
    tracker = TrendTracker(URL, "A Light in the Attic")

    
EXAMPLE of Selenium use website (DYNAMIC)
URL = "htts://www.nike.com/t/boston-celtics-city-edition-mens-nba-premium-jacket-3G9NyukK/HQ5759-010
    custom header for dynamic sites like NIKE

## 📦 Installation & Usage

1. **Clone the project:**
   ```bash
   git clone https://github.com/CheickLy/WatchIT.git
   cd Trend-Scraper
   ```

2.**Download required assets**
```bash
   pip install -r requirements.txt
```
3. 
