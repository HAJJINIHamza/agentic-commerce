import pandas as pd
from src.logger import get_logger

logger = get_logger(__name__)

class ContactSupplier:
    def __init__(self):
        pass

    def get_contacting_mail(self, 
                            product_name,
                            product_cost,
                            moq):
        """
        Generate an email to send to a supplier
        """

        email_template = """
            Hello,

            We are an e-commerce business based in Korea that sells Korean beauty, skincare, body care products, and related accessories to international markets, particularly Singapore.

            We are currently sourcing a {product_name} and are interested in your product. We would appreciate it if you could provide us with the following information:

            1. Unit cost and MOQ : Can you confirm that the unit price is {product_cost} usd for an moq of {moq} pieces ?
            2. Shipping to Singapore : Can you ship this product directly to Singapore ? If yes, please provide the available shipping methods, estimated delivery time, and shipping cost.

            We are interested in establishing a long-term business relationship with reliable suppliers, so we would be happy to discuss further cooperation if your product and terms are suitable for our business.

            Please feel free to send us your product catalog or other relevant information as well.

            Best regards,

            Hamza
            LLMCOREAI
        """
        
        email = email_template.format(
            product_name = product_name,
            product_cost = product_cost,
            moq = moq
        )

        return email
    