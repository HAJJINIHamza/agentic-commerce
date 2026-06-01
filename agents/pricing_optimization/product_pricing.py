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
        
        total_rate = self.compute_total_rate(product_id)
        if total_rate is None:
            logger.info("Total rate is 1 or more, cannot compute the selling price.")
            return None
        
        fixed_cost = self.compute_fixed_cost(product_id)

        product_price = fixed_cost / (1 - total_rate)

        self.product_selling_dict["selling_price"] = round(product_price, 2)
        logger.info(f"Selling price for product_id {product_id} is: {round(product_price, 2)}")
        logger.info(f"Product selling dict : {self.product_selling_dict}")
        return round(product_price, 2  )

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
        if total_rate >= 1:
            logger.info("Total rate is 1 or more, impossible to make profit from this product.")
            return None
        return total_rate
    
    #Simulate profit and margin given selling price 
    def simulate_profit(self, product_id, simulated_selling_price ):
        """
        Simulate profit and margin for a given selling price
        """
    
        if simulated_selling_price <= 0:
            raise ValueError ("Invalid value for simulated_selling_price, param should be > 0")

        total_rate = self.product_selling_dict.get("total_rate", self.compute_total_rate(product_id))
        fixed_cost = self.product_selling_dict.get("fixed_cost", self.compute_fixed_cost(product_id))

        net_revenue = simulated_selling_price * (1 - total_rate)
        profit = net_revenue - fixed_cost
        margin = profit / simulated_selling_price 

        self.product_selling_dict["simulation_{simulated_selling_price}"] = {
            "simulated_selling_price": simulated_selling_price,
            "profit": profit,
            "margin": margin
        }

        logger.info(f"Simulation for selling price {simulated_selling_price} : \
                        profit is {round(profit, 2)}, margin is {round(margin, 2)  }")
        
        return round(profit, 2), round(margin, 2)
    
    #Simulate selling price given margin
    def simulate_selling_price_given_margin (self, product_id, margin):
        """
        Simulate selling price for a given margin
        Answering the question : At what price should we sell to make this margin ?
        """

        fixed_cost = self.product_selling_dict.get("fixed_cost", self.compute_fixed_cost(product_id))
        total_rate = self.product_selling_dict.get("total_rate", self.compute_total_rate(product_id))

        if total_rate + margin >= 1:
            logger.info("Total rate + margin is 1 or more, impossible to make this margin from product")
            return None
            
        simulated_selling_price = fixed_cost / (1 - total_rate - margin)

        self.product_selling_dict["simulation_margin_{margin}"] = {
            "margin": margin,
            "simulated_selling_price": round(simulated_selling_price, 2)
        }

        return round(simulated_selling_price, 2) 



        


