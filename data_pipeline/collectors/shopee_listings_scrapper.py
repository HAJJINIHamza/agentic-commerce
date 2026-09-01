from bs4 import BeautifulSoup
import re
from pathlib import Path
import pandas as pd 
import json 

from src.logger import get_logger 

logger = get_logger(__name__)


def get_product_listings_from_page(product_id, product_name, html_file, ):
    """
    Extract the number of competitors from a Shopee search-results HTML file.

    A product is considered a competitor if at least one word from
    product_name appears in the product card title.

    Returns:
        dict containing:
        - number_of_competitors
    """

    # Read HTML file
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Split product name into individual words
    product_words = product_name.lower().split()
    print ("Product words:", product_words)

    # Find all Shopee product cards
    product_cards = soup.select(
        'li.shopee-search-item-result__item[data-sqe="item"]'
    )

    list_of_titles = []

    for card in product_cards:

        # Get product card title
        title_element = card.select_one(
        'div[role="group"][aria-label^="Product card:"]'
        )

        if title_element:
            card_title = title_element.get("aria-label")
            print ("Card title:", card_title)
            card_title = card_title.replace("Product card: ", "", 1).lower()
            list_of_titles.append(card_title)

    return {
        "id": product_id,
        "product_name": product_name,
        "number_of_titles": len(list_of_titles),
        "list_of_titles": list_of_titles
    }


if __name__ == "__main__":
    html_file = "data/scrapping/html_pages/7/shopee_selling_price_pages/product_7_shopee_page_1.html"
    result = get_product_listings_from_page(7, "Sheet_mask", html_file)
    print (result)