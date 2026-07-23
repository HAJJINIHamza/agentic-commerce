from bs4 import BeautifulSoup
import re
from pathlib import Path

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

    return {
        "id":id,
        "product_name": product_name,
        "prices": prices,
        "number_of_products": len(prices),
        "avg_selling_price": round(sum(prices) / len(prices), 2)
    }



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
        "sold_units": sold_units,
        "number_of_products": len(sold_units),
        "number_of_orders": number_of_orders
    }

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
        "ratings": ratings,
        "number_of_products": len(ratings),
        "average_product_rating": round(average_product_rating, 2)
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

    return {
        "id":id,
        "product_name": product_name,
        "number_of_pages": number_of_pages,
        "avg_selling_price": round(avg_selling_price, 2)
    }


#test
if __name__ == "__main__":
    html_file = "data/scrapping/html_pages/test - desk organizer - Prices and Deals - Jul 2026 _ Shopee Singapore.html"
    #result = extract_avg_selling_price_from_page(1213, "Desk organizer", html_file)
    #result = extract_number_of_orders_from_page(1213, "Desk organizer", html_file)
    #result = extract_average_product_rating_from_page(1213, "Desk organizer", html_file)
    result = get_avg_selling_price(19, "Desk organizer")
    print(result)
