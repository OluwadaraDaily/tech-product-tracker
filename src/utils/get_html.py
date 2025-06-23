import requests

def get_html(url: str) -> str:
    response = requests.get(url)
    return response.text