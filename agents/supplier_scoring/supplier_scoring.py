import pandas as pd 
import numpy as np
from math import log

from src.logger import get_logger

logger = get_logger()

class supplierScoringAgent:
    def __init__(self, supplier_data: pd.DataFrame):
        self.supplier_data = supplier_data
        # Ensure that numeric columns are in the correct format
        num_columns = [col for col in self.supplier_data.columns if col not in \
                       ["id", "product_name", "product_category", "supplier_name"]]
        self.supplier_data[num_columns] = (self.supplier_data[num_columns]
                                        .replace(",", ".", regex=True)
                                        .apply(pd.to_numeric, errors="coerce"))
        self.supplier_score_dict = {}
        

    def compute_supplier_score(self, supplier_id):
        """
        Computes the supplier reliability score for a product
        """
        logger.info ("Computing supplier score")
        supplier_rating_score = self.compute_supplier_rating_score(supplier_id)
        moq_score = self.compute_moq_score(supplier_id)
        supplier_response_rate_score = self.compute_supplier_response_rate_score(supplier_id)
        order_volume_score = self.compute_order_volume_score(supplier_id)

        supplier_score = (0.3 * supplier_rating_score + 
                                    0.3 * moq_score + 
                                    0.2 * supplier_response_rate_score + 
                                    0.2 * order_volume_score)
        
        classification = self.classify_supplier(supplier_id, supplier_score)

        self.supplier_score_dict =  {
            "supplier_score" : supplier_score,
            "supplier_rating_score": supplier_rating_score,
            "moq_score": moq_score,
            "supplier_response_rate_score": supplier_response_rate_score,
            "order_volume_score": order_volume_score,
            "classification": classification
        }

        logger.info (f"Supplier {supplier_id} score is : {supplier_score}")
        logger.info (f"Supplier score details : {self.supplier_score_dict}")
        return supplier_score, self.supplier_score_dict
    
    def compute_supplier_rating_score(self, supplier_id):
        """
        Computes the supplier rating score for a product
        """
        print ("Computing supplier rating score")
        supplier_rating = self.supplier_data.loc[self.supplier_data["supplier_id"] == supplier_id, 
                                            "supplier_rating"].values[0]

        supplier_rating_score = supplier_rating / 5
        print ("supplier_rating_score is : ", supplier_rating_score)
        return supplier_rating_score

    def compute_moq_score(self, supplier_id):
        """
        Computes the minimum order quantity score for a product
        """
        print ("Computing MOQ score")
        moq = self.supplier_data.loc[self.supplier_data["supplier_id"] == supplier_id, 
                                    "moq"].values[0]
        
        if moq <= 1:
            logger.info(f"Supplier MOQ is {moq}. This is perfect but rare.")
            return 1 

        moq_score = 1 / log(moq + 1)
        print (f"moq_score is : {moq_score}")
        return moq_score

    def compute_supplier_response_rate_score(self, supplier_id):
        """
        Computes the supplier response rate score for a product
        """
        print ("Computing supplier response rate score")
        response_rate = self.supplier_data.loc[self.supplier_data["supplier_id"] == supplier_id, 
                                            "supplier_response_rate"].values[0]
        supplier_response_rate_score = response_rate / 100

        print (f"supplier response rate score is : {supplier_response_rate_score}")

        return supplier_response_rate_score

    def compute_order_volume_score(self, supplier_id):
        """
        Computes the order volume score for a product
        """
        print ("Computing order volume score")
        supplier_completed_orders = self.supplier_data.loc[self.supplier_data["supplier_id"] == supplier_id, 
                                        "supplier_completed_orders"].values[0]
        supplier_max_orders = self.supplier_data.loc[self.supplier_data["supplier_id"] == supplier_id, 
                                            "supplier_max_orders"].values[0]

        if supplier_max_orders == 0:
            logger.info(f"Supplier has no orders so far for supplier_id {supplier_id}")
            return 0

        order_volume_score = log(supplier_completed_orders + 1) / log(supplier_max_orders + 1)

        print (f"order volume score is : {order_volume_score}")
        return order_volume_score
    
    def classify_supplier(self,supplier_id, supplier_score):
        """
        Classify supplier depending on score
        """
        if supplier_score >= 0.85:
            classification = "Excelent"
        
        elif supplier_score >= 0.7:
            classification = "Qualified"
        
        elif supplier_score >= 0.55:
            classification = "Review"
        
        else :
            classification = "Avoid"
        
        logger.info(f"Supplier {supplier_id}'s class is : {classification}")
        return classification
