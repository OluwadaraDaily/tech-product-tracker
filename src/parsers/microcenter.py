from bs4 import BeautifulSoup

def parse_microcenter_html(beautiful_soup_object: BeautifulSoup) -> dict:
    data = []
    # Get all the product cards
    product_cards_container = beautiful_soup_object.find("article", id="productGrid")
    product_cards = product_cards_container.find_all("li", class_="product_wrapper")

    # Get the product name, price, and link for each product card
    for product_card in product_cards:
        product_name = product_card.find("div", class_="h2").find("a").text.strip()
        product_price = product_card.find("span", itemprop="price").contents[2].text.strip()
        product_link = product_card.find("div", class_="h2").find("a")["href"]
        product_link = "https://www.microcenter.com" + product_link
        product_image = product_card.find("div", class_="result_left").find("img")["src"]

        data.append({
            "name": product_name,
            "price": product_price,
            "link": product_link,
            "image": product_image
        })

    return data