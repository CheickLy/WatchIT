🔍 Scraping Strategy & Design Decisions

Some modern websites (e.g., Nike) are built as Single Page Applications (SPAs), where content is rendered dynamically via JavaScript rather than delivered as static HTML.

For these sites, traditional tools like requests and BeautifulSoup may not reliably extract data because the HTML content is loaded after the initial page request. In such cases, browser automation tools like Selenium are more appropriate, as they allow JavaScript to fully execute before scraping. Beautiful soups reads the javascript as a "blank sheet" making it unable to scrape the information needed from said sites.

Additionally, large companies often use bot-detection services (e.g., Cloudflare) and frequently changing CSS class names. To improve scraping stability, this project prioritizes HTML data attributes and other consistent selectors when available, rather than relying on brittle CSS class names.

This approach improves maintainability and reduces breakage when site layouts change.

EXAMPLE of BeautifulSoup use website
URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html" 
    tracker = TrendTracker(URL, "A Light in the Attic")
EXAMPLE of Selenium use website
URL = "htts://www.nike.com/t/boston-celtics-city-edition-mens-nba-premium-jacket-3G9NyukK/HQ5759-010
    tracker = [....]
