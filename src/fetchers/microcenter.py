from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from config import SCRAPE_TARGETS
import asyncio

async def fetch_microcenter_html(search_param: str) -> BeautifulSoup:
    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Go to Microcenter homepage
        await page.goto(SCRAPE_TARGETS["microcenter"])
        
        # Find and fill the search input
        await page.fill('input[id="search-query"]', search_param)
        
        # Press Enter to submit the search
        await page.press('input[id="search-query"]', 'Enter')
        
        # Wait for the search results to load
        # Adjust the selector based on Microcenter's actual page structure
        await page.wait_for_selector('.product_wrapper')
        
        # Add a small delay to ensure all dynamic content is loaded
        await asyncio.sleep(3)
        
        # Get the page content
        html = await page.content()
        
        # Close the browser
        await browser.close()
        
        return BeautifulSoup(html, 'html.parser')

if __name__ == "__main__":
    asyncio.run(fetch_microcenter_html())