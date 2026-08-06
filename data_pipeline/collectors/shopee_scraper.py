from bs4 import BeautifulSoup
import re
from pathlib import Path
import pandas as pd 
import json 

from src.logger import get_logger 

logger = get_logger(__name__)

def extract_avg_selling_price_from_page(id, product_name, html_file):
    """
    Extract product prices from a Shopee search-results HTML file.

    Returns:
        dict containing:
        - prices
        - number_of_products
        - avg_selling_price
    """

    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    print ("Read HTML file")
    soup = BeautifulSoup(html, "html.parser")
    prices = []

    product_cards = soup.select(
        'li.shopee-search-item-result__item[data-sqe="item"]'
    )
    for card in product_cards:

        text = card.get_text(" ", strip=True)

        # Extract all monetary values in this product card
        matches = re.findall(
            r'\$\s*([\d,]+(?:\.\d{1,2})?)',
            text
        )

        if matches:
            price = float(matches[0].replace(",", ""))
            prices.append(price)
    
    if not prices:
        return {
            "prices": [],
            "number_of_products": 0,
            "avg_selling_price": None
        }

    print (f"avg_selling_price: {round(sum(prices) / len(prices), 2)}")

    return {
        "id":id,
        "product_name": product_name,
        "prices": prices,
        "number_of_products": len(prices),
        "avg_selling_price": round(sum(prices) / len(prices), 2)
    }


def get_avg_selling_price(id, product_name):
    """
    Get the average selling price of a product by aggregating data from multiple Shopee HTML pages.
    """

    pages_path = f"data/scrapping/html_pages/{id}/selling_price_pages/"
    pages_path = Path(pages_path)
    if not pages_path.exists():
        raise FileNotFoundError(f"Directory not found: {pages_path}")
    
    print ("Pages path:", pages_path)
    selling_prices = []
    number_of_pages = 0

    for html_file in pages_path.glob("*.html"):
        print ("Html file :", html_file)
        number_of_pages += 1
        result = extract_avg_selling_price_from_page(id, product_name, html_file)
        page_avg_selling_price = result["avg_selling_price"]
        selling_prices.append(page_avg_selling_price)
        print(f"Processed {html_file}: {result}")
    
    avg_selling_price = sum(selling_prices)/len(selling_prices) if selling_prices else None

    js_result = {
        "id":id,
        "product_name": product_name,
        "number_of_pages": number_of_pages,
        "avg_selling_price": round(avg_selling_price, 2)
    }

    logger.info(f"Average selling price result for product {id} is {js_result["avg_selling_price"]}" )

    return js_result

# ------------------------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------------------------

def extract_number_of_orders_from_page(id, product_name, html_file):
    """
    Extract the number of sold units from all Shopee product cards
    and sum them to get the total number of orders.

    Conversion examples:
        "163 sold"  -> 163
        "950 sold"  -> 950
        "2k+ sold"  -> 2000
        "4k+ sold"  -> 4000

    Args:
        html_file (str): Path to the Shopee HTML file.

    Returns:
        dict:
            {
                "id": int,
                "product_name": str,
                "sold_units": [...],
                "number_of_products": int,
                "number_of_orders": int
            }
    """

    # Read HTML file
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    sold_units = []

    # Find all Shopee product cards
    product_cards = soup.select(
        'li.shopee-search-item-result__item[data-sqe="item"]'
    )

    for card in product_cards:
        # Find text containing "sold"
        sold_element = card.find(
            string=re.compile(r'\bsold\b', re.IGNORECASE)
        )
        if sold_element:
            sold_text = sold_element.strip().lower()

            # Extract number before "sold"
            match = re.search(
                r'([\d,.]+)\s*([km]?)\+?\s*sold',
                sold_text
            )

            if match:
                number = float(match.group(1).replace(",", ""))
                multiplier = match.group(2)

                # Convert k / m
                if multiplier == "k":
                    number *= 1_000
                elif multiplier == "m":
                    number *= 1_000_000

                sold_units.append(int(number))

    # Sum all sold units
    number_of_orders = sum(sold_units)

    return {
        "id": id,
        "product_name": product_name,
        "sold_units": sold_units,
        "number_of_products": len(sold_units),
        "number_of_orders": number_of_orders
    }

def get_number_of_orders(id, product_name):
    """"
    Get the total number of orders for a product by aggregating data from multiple Shopee HTML pages.
    """
    pages_path = f"data/scrapping/html_pages/{id}/selling_price_pages/"
    pages_path = Path(pages_path)
    if not pages_path.exists():
        raise FileNotFoundError(f"Directory not found: {pages_path}")
    
    number_of_orders = []
    number_of_pages = 0

    for html_file in pages_path.glob("*.html"):
        print ("Html file :", html_file)
        number_of_pages += 1
        result = extract_number_of_orders_from_page(id, product_name, html_file)
        page_number_of_orders = result["number_of_orders"]
        number_of_orders.append(page_number_of_orders)
        print(f"Processed {html_file}: {result}")
    
    total_number_of_orders = sum(number_of_orders) if number_of_orders else None

    js_result = {
        "id":id,
        "product_name": product_name,
        "number_of_pages": number_of_pages,
        "total_number_of_orders": total_number_of_orders
    }

    logger.info(f"Total number of orders result for product {id} is {js_result["total_number_of_orders"]}" )

    return js_result

# ------------------------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------------------------

def extract_average_product_rating_from_page(id, product_name, html_file):
    """
    Extract product ratings from all Shopee product cards
    and calculate the average product rating.

    Args:
        id (int): Product ID.
        product_name (str): Name of the product.
        html_file (str): Path to the Shopee HTML file.

    Returns:
        dict:
            {
                "ratings": [...],
                "number_of_products": int,
                "average_product_rating": float
            }
    """

    # Read HTML file
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    ratings = []

    # Find all Shopee product cards
    product_cards = soup.select(
        'li.shopee-search-item-result__item[data-sqe="item"]'
    )

    for card in product_cards:

        # Get all text inside the product card
        text = card.get_text(" ", strip=True)

        # Look for rating values between 0 and 5
        # Examples: 4.8, 4.5, 5.0
        matches = re.findall(
            r'(?<![\d.])([0-5]\.\d)(?![\d.])',
            text
        )

        if matches:
            # The first matching decimal is assumed to be the product rating
            rating = float(matches[0])

            # Safety check
            if 0 <= rating <= 5:
                ratings.append(rating)

    # Calculate average rating
    if not ratings:
        return {
            "ratings": [],
            "number_of_products": 0,
            "average_product_rating": None
        }

    average_product_rating = sum(ratings) / len(ratings)

    return {
        "id": id,
        "product_name": product_name,
        "ratings": ratings,
        "number_of_products": len(ratings),
        "average_product_rating": round(average_product_rating, 2)
    }

def get_average_product_rating(id, product_name):
    """
    Get the average product rating of a product by aggregating data from multiple Shopee HTML pages.
    """

    pages_path = f"data/scrapping/html_pages/{id}/selling_price_pages/"
    pages_path = Path(pages_path)
    if not pages_path.exists():
        raise FileNotFoundError(f"Directory not found: {pages_path}")
    
    ratings = []
    number_of_pages = 0

    for html_file in pages_path.glob("*.html"):
        print ("Html file :", html_file)
        number_of_pages += 1
        result = extract_average_product_rating_from_page(id, product_name, html_file)
        page_average_product_rating = result["average_product_rating"]
        ratings.append(page_average_product_rating)
        print(f"Processed {html_file}: {result}")
    
    average_product_rating = sum(ratings)/len(ratings) if ratings else None

    js_result = {
        "id":id,
        "product_name": product_name,
        "number_of_pages": number_of_pages,
        "average_product_rating": round(average_product_rating, 2)
    }

    logger.info(f"Average product rating result for product {id} is {js_result["average_product_rating"]}" )

    return js_result

# ------------------------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------------------------

def get_search_three_month_growth(id, product_name):
    """
    Get the search three-month growth of a product by aggregating data from multiple Shopee HTML pages.
    """
    
    df = pd.read_csv("data/scrapping/data_tables/search_three_months_growth_04-08-2026.csv", sep= ";")
    search_three_month_growth = df[df["id"] == id]["search_three_month_growth"].values[0]
    logger.info(f"Search three-month growth result for product {id} is {search_three_month_growth}" )

    return {
        "id": id,
        "product_name": product_name,
        "search_three_month_growth": search_three_month_growth
    }

# ------------------------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------------------------

def get_fixed_variables():
    with open("data_pipeline/config/product_config.json", "r") as f:
        fixed_variables = json.load(f)

    return fixed_variables

# ------------------------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------------------------

def get_number_of_competitors_from_page(id, product_name, html_file):
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

    number_of_competitors = 0

    for card in product_cards:

        # Get product card title
        title_element = card.select_one(
        'div[role="group"][aria-label^="Product card:"]'
        )

        if title_element:
            card_title = title_element.get("aria-label")
            print ("Card title:", card_title)
            card_title = card_title.replace("Product card: ", "", 1).lower()

            if any(word in card_title for word in product_words):
                number_of_competitors += 1

    return {
        "id": id,
        "product_name": product_name,
        "number_of_competitors": number_of_competitors
    }

def get_number_of_competitors(id, product_name):
    """
    Get the number of competitors for a product by aggregating data from multiple Shopee HTML pages.
    """
    
    pages_path = f"data/scrapping/html_pages/{id}/selling_price_pages/"
    pages_path = Path(pages_path)
    if not pages_path.exists():
        raise FileNotFoundError(f"Directory not found: {pages_path}")
    
    number_of_competitors_list = []
    number_of_pages = 0

    for html_file in pages_path.glob("*.html"):
        print ("Html file :", html_file)
        number_of_pages += 1
        result = get_number_of_competitors_from_page(id, product_name, html_file)
        page_number_of_competitors = result["number_of_competitors"]
        number_of_competitors_list.append(page_number_of_competitors)
        print(f"Processed {html_file}: {result}")
    
    total_number_of_competitors = sum(number_of_competitors_list) if number_of_competitors_list else None

    js_result = {
        "id":id,
        "product_name": product_name,
        "number_of_pages": number_of_pages,
        "total_number_of_competitors": total_number_of_competitors
    }

    logger.info(f"Total number of competitors result for product {id} is {js_result}" )

    return js_result

# ------------------------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------------------------


from bs4 import BeautifulSoup
import re


def get_avg_product_cost_from_page(id, product_name, html_file):
    """
    Extract product costs from Alibaba product cards whose title
    contains at least one word from product_name.

    For price ranges, the highest price is used:
        $7.74       -> 7.74
        $7.74-9.70  -> 9.70

    Returns:
        dict containing:
        - product_costs
        - avg_product_cost
    """

    # Read HTML file
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Split product name into individual words
    product_words = product_name.lower().split()

    product_costs = []

    # Find all Alibaba product cards
    product_cards = soup.select(
        'div.fy26-product-card-content'
    )

    for card in product_cards:

        # Get product title
        title_element = card.select_one(
            'h2.searchx-product-e-title'
        )

        if not title_element:
            continue

        card_title = title_element.get_text(
            " ", strip=True
        ).lower()

        # Check if at least one product-name word
        # exists in the product title
        if any(word in card_title for word in product_words):

            # Find product price
            price_element = card.select_one(
                'div.searchx-product-price-price-main'
            )

            if not price_element:
                continue

            price_text = price_element.get_text(
                " ", strip=True
            )

            # Extract ALL prices from the price text
            # Example:
            # "$7.74"       -> ["7.74"]
            # "$7.74-9.70"  -> ["7.74", "9.70"]
            matches = re.findall(
                r'\$?\s*([\d,]+(?:\.\d{1,2})?)',
                price_text
            )

            if matches:
                # Convert prices to floats
                prices = [
                    float(price.replace(",", ""))
                    for price in matches
                ]

                # Use the highest price
                product_cost = max(prices)

                product_costs.append(product_cost)

    # Calculate average
    if product_costs:
        avg_product_cost = sum(product_costs) / len(product_costs)
    else:
        avg_product_cost = None

    return {
        "id": id,
        "product_name": product_name,
        "product_costs": product_costs,
        "avg_product_cost": avg_product_cost
    }

def get_avg_product_cost(id, product_name):
    """
    Get the average product cost of a product by aggregating data from multiple Alibaba HTML pages.
    """

    pages_path = f"data/scrapping/html_pages/{id}/alibaba_pages/"
    pages_path = Path(pages_path)
    if not pages_path.exists():
        raise FileNotFoundError(f"Directory not found: {pages_path}")
    
    product_costs = []
    number_of_pages = 0

    for html_file in pages_path.glob("*.html"):
        print ("Html file :", html_file)
        number_of_pages += 1
        result = get_avg_product_cost_from_page(id, product_name, html_file)
        page_avg_product_cost = result["avg_product_cost"]
        if page_avg_product_cost is not None:
            product_costs.append(page_avg_product_cost)
        print(f"Processed {html_file}: {result}")
    
    avg_product_cost = sum(product_costs)/len(product_costs) if product_costs else None

    js_result = {
        "id":id,
        "product_name": product_name,
        "number_of_pages": number_of_pages,
        "avg_product_cost": round(avg_product_cost, 2) if avg_product_cost is not None else None
    }

    logger.info(f"Average product cost result for product {id} is {js_result['avg_product_cost']}" )

    return js_result
    

#test
if __name__ == "__main__":
    html_file = "data/scrapping/html_pages/19/selling_price_pages/product_19_shopee_page_1.html"
    alibaba_html_file = "data/scrapping/html_pages/19/alibaba_pages/product_19_alibaba_page_1.html"
    #result = extract_avg_selling_price_from_page(1213, "Desk organizer", html_file)
    #result = extract_number_of_orders_from_page(1213, "Desk organizer", html_file)
    #result = extract_average_product_rating_from_page(1213, "Desk organizer", html_file)
    #result = get_avg_selling_price(19, "Desk organizer")
    #result = get_number_of_orders(19, "Desk organizer")
    #result = get_average_product_rating(19, "Desk organizer")
    #result = get_search_three_month_growth(19, "Desk organizer")
    #result = get_number_of_competitors_from_page(19, "Desk organizer", html_file)
    #result = get_number_of_competitors(19, "Desk organizer")
    result = get_avg_product_cost_from_page(19, "Desk organizer", alibaba_html_file)
    print(result)
