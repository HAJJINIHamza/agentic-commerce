from bs4 import BeautifulSoup
import re
from pathlib import Path
import pandas as pd 
import json 

from src.logger import get_logger 

logger = get_logger(__name__)


def get_product_titles_from_page(product_id, product_name):
    """
    Extract product titles from a Shopee search-results HTML file.

    A product is considered a competitor if at least one word from
    product_name appears in the product card title.

    Params:
    - Make sure that the html file is following this logic : data/scrapping/html_pages/{product_id}/shopee_selling_price_pages/product_{product_id}_shopee_page_1.html

    Returns:
        dict containing:
        - number_of_competitors
    """
    html_file = Path(f"data/scrapping/html_pages/{product_id}/shopee_selling_price_pages/product_{product_id}_shopee_page_1.html")

    if not html_file.exists():
        logger.error(f"HTML file not found: {html_file}")
        raise FileNotFoundError(f"HTML file not found: {html_file}")

    # Read HTML file
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Split product name into individual words
    product_words = product_name.lower().split()

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
            # print ("Card title:", card_title)
            card_title = card_title.replace("Product card: ", "", 1).lower()
            list_of_titles.append(card_title)

    return {
        "id": product_id,
        "product_name": product_name,
        "number_of_titles": len(list_of_titles),
        "list_of_titles": list_of_titles
    }

def get_product_description_from_page(product_id, product_name, html_file):
    """
    Extract the text from the Product Description section of a Shopee
    product page HTML file.

    Images inside the description are ignored.

    Params:
    - product_id: Product ID used to locate the HTML file.

    HTML file must follow this structure:
    data/scrapping/html_pages/{product_id}/shopee_description_pages/
        product_{product_id}_shopee_description_page_{page_number}.html

    Returns:
        dict containing:
        - id
        - description
    """

    #html_file = Path(
    #    f"data/scrapping/html_pages/{product_id}/"
    #    f"shopee_description_pages/"
    #    f"{html_file}"
    #)

    if not html_file.exists():
        logger.error(f"HTML file not found: {html_file}")
        raise FileNotFoundError(f"HTML file not found: {html_file}")

    # Read HTML
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Find the "Product Description" heading
    description_heading = soup.find(
        "h2",
        string=lambda text: text and text.strip() == "Product Description"
    )

    if not description_heading:
        logger.warning(
            f"Product Description section not found for product {product_id}"
        )
        return {
            "id": product_id,
            "product_name": product_name,  
            "description": ""
        }

    # Get the section containing the Product Description
    description_section = description_heading.find_parent("section")

    if not description_section:
        logger.warning(
            f"Product Description section container not found "
            f"for product {product_id}"
        )
        return {
            "id": product_id,
            "product_name": product_name,
            "description": ""
        }

    # Remove images so that only textual content remains
    for element in description_section.find_all(
        ["img", "picture", "source", "video"]
    ):
        element.decompose()

    # Extract text from paragraphs
    paragraphs = description_section.find_all("p")

    description_parts = []

    for paragraph in paragraphs:
        text = paragraph.get_text(" ", strip=True)

        if text:
            description_parts.append(text)

    description = "\n".join(description_parts)

    return {
        "id": product_id,
        "product_name": product_name,
        "description": description
    }

def get_product_description_from_all_pages(product_id, product_name):
    """
    Extract the text from the Product Description section of all Shopee
    product page HTML files for a given product.

    Params:
    - product_id: Product ID used to locate the HTML files.

    HTML files must follow this structure:
    data/scrapping/html_pages/{product_id}/shopee_description_pages/
        product_{product_id}_shopee_description_page_{page_number}.html

    Returns:
        dict containing:
        - id
        - descriptions: list of dicts with page_number and description
    """

    descriptions = []
    pages_path = f"data/scrapping/html_pages/{product_id}/shopee_description_pages/"
    pages_path = Path(pages_path)
    if not pages_path.exists():
        raise FileNotFoundError(f"Directory not found: {pages_path}")
    
    nbr_of_pages = 0
    for html_file in pages_path.glob("*.html"):
        nbr_of_pages += 1
        description_dict = get_product_description_from_page(product_id, product_name, html_file)
        descriptions.append(description_dict["description"])

    log_info = {"id": product_id, "product_name": product_name, "number_of_pages": nbr_of_pages}
    logger.info(f"Extracted descriptions from all pages for product : {product_id}: {log_info}")

    return {
        "id": product_id,
        "product_name": product_name,
        "number_of_pages": nbr_of_pages,
        "descriptions": descriptions
    }



if __name__ == "__main__":
    #result = get_product_titles_from_page("7", "Sheet_mask")
    #result = get_product_description_from_page("7", "Sheet_mask", html_file="product_7_shopee_description_page_2.html")
    result = get_product_description_from_all_pages("7", "Sheet_mask")
    print (result)