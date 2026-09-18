import pandas as pd 
import numpy as np
from math import log, exp

from src.logger import get_logger

logger = get_logger()

class supplierScoringAgent:
    def __init__(self, supplier_data: pd.DataFrame):
        self.supplier_data = supplier_data
        # Ensure that numeric columns are in the correct format
        num_columns = [col for col in self.supplier_data.columns if col not in \
                       ["id", "product_name", "product_category", "supplier_name", 
                        "supplier_id", "product_id", "supplier_name", "product_name", 
                        "supplier_product_name", "place_of_origin", "supplier_url"
                        ]]
        self.supplier_data[num_columns] = (self.supplier_data[num_columns]
                                        .replace(",", ".", regex=True)
                                        .apply(pd.to_numeric, errors="coerce"))
        self.supplier_score_dict = {}
        

    def compute_supplier_score(self, supplier_id):
        """
        Computes the supplier reliability score for a product
        """
        logger.info ("Computing supplier score")
        #supplier_rating_score = self.compute_supplier_rating_score(supplier_id)
        supplier_product_cost_score = self.compute_supplier_product_cost_score(supplier_id)
        moq_score = self.compute_moq_score(supplier_id)
        supplier_tenure_score = self.compute_supplier_tenure_score(supplier_id)
        place_of_origin_score = self.compute_place_of_origin_score(supplier_id)
        supplier_response_time_score = self.compute_supplier_response_time_score(supplier_id)
        images_quality_score = self.compute_supplier_images_quality(supplier_id)
        #order_volume_score = self.compute_order_volume_score(supplier_id)

        supplier_score = (0.4 * supplier_product_cost_score
                          + 0.3 * moq_score
                          + 0.1 * images_quality_score
                          + 0.05 * supplier_tenure_score
                          + 0.05 * place_of_origin_score
                          + 0.1 * supplier_response_time_score)
        
        classification = self.classify_supplier(supplier_id, supplier_score)

        self.supplier_score_dict =  {
            "supplier_score" : supplier_score,
            "supplier_product_cost_score": supplier_product_cost_score,
            "moq_score": moq_score,
            "supplier_tenure_score": supplier_tenure_score,
            "place_of_origin_score": place_of_origin_score,
            "supplier_response_time_score": supplier_response_time_score,
            "images_quality_score": images_quality_score,
            "classification": classification
        }

        logger.info (f"Supplier {supplier_id} score is : {supplier_score}")
        logger.info (f"Supplier score details : {self.supplier_score_dict}")
        return supplier_score, self.supplier_score_dict
    
    def compute_supplier_product_cost_score(self, supplier_id):
        """
        Computes the score for the cost of a product from supplier_id
        """
        print ("Computing supplier product cost score")
        product_cost = self.supplier_data.loc[self.supplier_data["supplier_id"] == supplier_id, 
                                            "product_cost"].values[0]
        
        product_cost_score = 1/(1+ product_cost)
        product_cost_score = min(product_cost_score, 1)  # Cap the score at 1
        logger.info (f"Product cost score for supplier {supplier_id} is : {product_cost_score}")

        return product_cost_score
    
    def compute_place_of_origin_score(self, supplier_id):
        """
        Computes the score for the place of origin of a product from supplier_id
        """
        print ("Computing place of origin score")
        place_of_origin = self.supplier_data.loc[self.supplier_data["supplier_id"] == supplier_id, 
                                            "place_of_origin"].values[0]
        
        if place_of_origin is None:
            raise ValueError(f"Place of origin for supplier {supplier_id} is None  ")
        
        elif place_of_origin == "korea":
            place_of_origin_score = 1.0
        
        else : 
            place_of_origin_score = 0.1
        
        logger.info (f"Place of origin score for supplier {supplier_id} is : {place_of_origin_score}")

        return place_of_origin_score

    def compute_supplier_tenure_score(self, supplier_id):
        """
        Computes the score for the tenure of a supplier
        """

        supplier_tenure = self.supplier_data.loc[self.supplier_data["supplier_id"] == supplier_id,
                                            "supplier_tenure_y"].values[0]
        max_supplier_tenure = self.supplier_data["supplier_tenure_y"].max()

        if max_supplier_tenure == 0:
            raise ValueError(f"Max supplier tenure is zero, cannot compute tenurescore for supplier {supplier_id}")
        
        supplier_tenure_score = log(supplier_tenure + 1)/log(max_supplier_tenure + 1)

        logger.info (f"Supplier tenure score for supplier {supplier_id} is : {supplier_tenure_score}")
        return supplier_tenure_score
    
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
    
    def compute_supplier_response_time_score(self, supplier_id):
        """
        Computes the supplier response time score for a product
        """
        print ("Computing supplier response time score")
        response_time = self.supplier_data.loc[self.supplier_data["supplier_id"] == supplier_id, 
                                            "supplier_response_time_h"].values[0]
        supplier_response_time_score = 1 / (1 + response_time)

        print (f"supplier response time score is : {supplier_response_time_score}")

        return supplier_response_time_score
    
    def compute_supplier_images_quality(self, supplier_id):
        """"
        Computes the score for the images quality of a product from supplier_id
        """
        images_quality = self.supplier_data.loc[self.supplier_data["supplier_id"] == supplier_id,
                                            "images_quality"].values[0]
        
        images_quality_score = images_quality / 5  # Quality is rated from 1 to 5.

        logger.info (f"Images quality score for supplier {supplier_id} is : {images_quality_score}")
        return images_quality_score
    
    
    ### -------------------------------------------------------------------------
    ### Can't use the functions bellow for now because we don't have the data yet.
    ### -------------------------------------------------------------------------
    
    def compute_supplier_rating_score(self, supplier_id):
        """
        Computes the supplier rating score for a product
        """
        print ("Computing supplier rating score")
        supplier_rating = self.supplier_data.loc[self.supplier_data["supplier_id"] == supplier_id, 
                                            "supplier_rating"].values[0]

        supplier_rating_score = supplier_rating / 5
        print ("supplier_rating_score is : ", supplier_rating_score)
        logger.info ("supplier_rating_score is : ", supplier_rating_score)

        return supplier_rating_score

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
