from bs4 import BeautifulSoup
from utils.get_html import get_html
from config import SCRAPE_TARGETS

def fetch_microcenter_html(search_param: str) -> dict:
    html = get_html(SCRAPE_TARGETS["microcenter"] + "&vkw=" + search_param)
    soup = BeautifulSoup(html, 'html.parser')
    return soup

if __name__ == "__main__":
    fetch_microcenter_html()