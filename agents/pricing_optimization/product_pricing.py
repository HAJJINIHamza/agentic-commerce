import pandas as pd 
from src.logger import get_logger

logger = get_logger(__name__)

class ProductSellingPriceAgent:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        # Ensure that numeric columns are in the correct format
        num_columns = [col for col in self.data.columns if col not in \
                       ["id", "product_name", "product_category"]]
        self.data[num_columns] = (self.data[num_columns]
                                        .replace(",", ".", regex=True)
                                        .apply(pd.to_numeric, errors="coerce"))
        self.product_selling_dict = {}

    def get_product_selling_price(self, product_id):
        """"
        Compute the selling price of a product
        """
        logger.info(f"Computing selling price for product {product_id}")

        self.product_selling_dict["product_id"] = product_id
        
        fixed_cost = self.compute_fixed_cost(product_id)
        total_rate = self.compute_total_rate(product_id)

        product_price = fixed_cost / (1 - total_rate)

        self.product_selling_dict["selling_price"] = product_price
        logger.info(f"Selling price for product_id {product_id} is: {product_price}")
        logger.info(f"Product selling dict : {self.product_selling_dict}")
        return product_price

    def compute_fixed_cost(self, product_id):
        """
        Compute the fixed cost of the product
        """
        product_cost = self.data.loc[self.data["id"] == product_id, "product_cost"].values[0]
        shipping_cost = self.data.loc[self.data["id"] == product_id, "shipping_cost"].values[0]
        packaging_cost = self.data.loc[self.data["id"] == product_id, "packaging_cost"].values[0]
        international_shipping_cost = self.data.loc[self.data["id"] == product_id, "international_shipping_cost"].values[0]
        platform_fees = self.data.loc[self.data["id"] == product_id, "platform_fees"].values[0]
        advertising_cost = self.data.loc[self.data["id"] == product_id, "advertising_cost"].values[0]
        payment_fees = self.data.loc[self.data["id"] == product_id, "payment_fees"].values[0]

        fixed_cost = ( product_cost
                        + shipping_cost
                        + packaging_cost
                        + international_shipping_cost
                        + platform_fees
                        + advertising_cost
                        + payment_fees
                        + advertising_cost )
        
        self.product_selling_dict["fixed_cost"] = fixed_cost
        self.product_selling_dict["fixed_cost_components"] = {
            "product_cost": product_cost,
            "shipping_cost": shipping_cost,
            "packaging_cost": packaging_cost,
            "international_shipping_cost": international_shipping_cost,
            "platform_fees": platform_fees,
            "advertising_cost": advertising_cost,
            "payment_fees": payment_fees
        }
        
        print (f"Fixed costs is: {fixed_cost}")
        return fixed_cost
        
    def compute_total_rate(self, product_id):
        """
        Compute the total rate of the product
        """
        commission_rate = self.data.loc[self.data["id"] == product_id, "commission_rate"].values[0]
        transaction_fee_rate = self.data.loc[self.data["id"] == product_id, "transaction_fee_rate"].values[0]
        payoneer_fee_rate = self.data.loc[self.data["id"] == product_id, "payoneer_fee_rate"].values[0]
        service_fee_rate = self.data.loc[self.data["id"] == product_id, "service_fee_rate"].values[0]
        ad_cost_rate = self.data.loc[self.data["id"] == product_id, "ad_cost_rate"].values[0]
        target_margin_rate = self.data.loc[self.data["id"] == product_id, "target_margin_rate"].values[0]

        total_rate = (commission_rate 
                    + transaction_fee_rate 
                    + payoneer_fee_rate 
                    + service_fee_rate 
                    + ad_cost_rate 
                    + target_margin_rate )
        
        self.product_selling_dict["total_rate"] = total_rate
        self.product_selling_dict["total_rate_components"] = {
            "commission_rate": commission_rate,
            "transaction_fee_rate": transaction_fee_rate,
            "payoneer_fee_rate": payoneer_fee_rate,
            "service_fee_rate": service_fee_rate,
            "ad_cost_rate": ad_cost_rate,
            "target_margin_rate": target_margin_rate
        }
        print (f"Total rate is: {total_rate}")
        return total_rate