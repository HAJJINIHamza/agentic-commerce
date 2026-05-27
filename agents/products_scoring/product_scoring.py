import pandas as pd 
from src.logger import get_logger

#logger
log = get_logger(__name__)

#Read products level 3 data 
products_data = pd.read_csv("data/products_list_iter_1.csv")

#This data is level 3 product information 
#Neet to go level 3 -> level 2 then level 2 -> level 1.

#TODO : you should add Try Except to all fuctions
#TODO : Add DataFrame savings at each level
#TODO : ADD unit tests

#level 0

def score_product(product_id):
    """
    Computes the final product score
    """
    demand_growth = compute_demand_growth(product_id)
    low_competition_score = compute_competition_score(product_id)
    expected_margin = compute_expected_margin(product_id)
    logistics_simplicity = compute_logistics_simplicity(product_id)
    supplier_reliability = compute_supplier_reliability(product_id)
    tiktok_virality = compute_tiktok_virality(product_id)
    compliance_safety = compute_compliance_safety(product_id)

    product_score = 0.25 * demand_growth 
                    + 0.2 * low_competition_score
                    + 0.2 * expected_margin 
                    + 0.1 * logistics_simplicity 
                    + 0.1 * supplier_reliability 
                    + 0.1 * tiktok_virality 
                    + 0.05 * compliance_safety
    log.info(f"Computed product score for product_id {product_id}: {product_score}")
    return product_score

# Level 1 metrics

def compute_demand_growth(product_id):
    """
    Computes the demand growth for a product
    """
    order_growth = products_data.loc[products_data["product_id"] == product_id, 
                                        "order_growth"].values[0]
    search_trend_growth = products_data.loc[products_data["product_id"] == product_id, 
                                        "search_trend_growth"].values[0]
    review_growth = products_data.loc[products_data["product_id"] == product_id, 
                                        "review_growth"].values[0]

    demand_growth = 0.5 * order_growth 
                    + 0.3 * search_trend_growth 
                    + 0.2 * review_growth
    
    return demand_growth

def compute_competition_score(product_id):
    """
    Computes the low competition score for a product
    """
    seller_density_score = compute_seller_density_score(product_id)
    review_saturation_score = compute_review_saturation_score(product_id)
    price_war_score = compute_price_war_score(product_id)

    low_competition_score = 0.5 * seller_density_score 
                         + 0.3 * review_saturation_score 
                         + 0.2 * price_war_score
    
    return low_competition_score

def compute_expected_margin(product_id):
    """
    Computes the expected margin for a product
    """
    selling_price = products_data.loc[products_data["product_id"] == product_id, 
                                        "avg_selling_price"].values[0]
    product_cost = products_data.loc[products_data["product_id"] == product_id, 
                                        "product_cost"].values[0]
    shipping_cost = products_data.loc[products_data["product_id"] == product_id,    
                                        "shipping_cost"].values[0]
    platform_fees = products_data.loc[products_data["product_id"] == product_id, 
                                        "platform_fees"].values[0]
    advertising_costs = products_data.loc[products_data["product_id"] == product_id, 
                                        "advertising_costs"].values[0]

    expected_margin = (selling_price
                       - product_cost
                       - shipping_cost
                       - platform_fees
                       - advertising_costs
                       ) / selling_price
    
    return expected_margin

def compute_logistics_simplicity(product_id):
    """
    Computes the logistics simplicity score for a product
    """
    delivery_time_score = compute_delivery_time_score(product_id)
    shipping_cost_score = compute_shipping_cost_score(product_id)
    weight_score = compute_size_weight_score(product_id)
    fragility_score = compute_fragility_score(product_id)

    logistics_simplicity_score = 0.4 * delivery_time_score +
                            0.3 * shipping_cost_score +
                            0.2 * weight_score +
                            0.1 * fragility_score
    
    return logistics_simplicity_score

def compute_supplier_reliability(product_id):
    """
    Computes the supplier reliability score for a product
    """
    supplier_rating_score = compute_supplier_rating_score(product_id)
    moq_score = compute_moq_score(product_id)
    supplier_response_rate_score = compute_supplier_response_rate_score(product_id)
    order_volume_score = compute_order_volume_score(product_id)

    supplier_reliability_score = 0.3 * supplier_rating_score +
                                0.3 * moq_score +
                                0.2 * supplier_response_rate_score +
                                0.2 * order_volume_score
    
    return supplier_reliability_score

def compute_tiktok_virality(product_id):
    """
    Computes the TikTok virality score for a product
    """
    trend_growth_score = compute_trend_growth_score(product_id)
    creator_adoption_score = compute_creator_adoption_score(product_id)

    tiktok_virality_score = 0.6 * trend_growth_score +
                           0.4 * creator_adoption_score +
    
    return tiktok_virality_score

def compute_compliance_safety(product_id):
    """
    Computes the compliance and safety score for a product
    """
    risk_level = compute_risk_level(product_id)

    compliance_safety_score = 1 - risk_level 
    
    return compliance_safety_score


#Level 2 metrics 

def compute_order_growth(product_id):
    """
    Computes the order growth for a product
    """
    order_this_month = products_data.loc[products_data["product_id"] == product_id, 
                                        "orders_this_month"].values[0]
    order_last_month = products_data.loc[products_data["product_id"] == product_id, 
                                        "orders_last_month"].values[0]
    
    if order_last_month == 0:
        if order_this_month != 0:
            log.info(f"Last month orders is 0 for product_id {product_id}, there is a 100% order growth")
            return 1    
        else :
            log.info(f"No order growth for product_id {product_id}")
            return 0

    order_growth = (order_this_month - order_last_month) / order_last_month 

    return order_growth

def compute_search_trend_growth(product_id):
    """
    Computes the search trend growth for a product
    """
    search_this_month = products_data.loc[products_data["product_id"] == product_id, 
                                        "search_this_month"].values[0]
    search_last_month = products_data.loc[products_data["product_id"] == product_id, 
                                        "search_last_month"].values[0]
    
    if search_last_month == 0:
        if search_this_month != 0:
            log.info(f"Last month search is 0 for product_id {product_id}, there is a 100% search trend growth")
            return 1    
        else :
            log.info(f"No search trend growth for product_id {product_id}")
            return 0

    search_trend_growth = (search_this_month - search_last_month) / search_last_month

    return search_trend_growth

def compute_review_growth(product_id):
    """
    Computes the review growth for a product
    """
    reviews_this_month = products_data.loc[products_data["product_id"] == product_id, 
                                             "reviews_this_month"].values[0]
    reviews_last_month = products_data.loc[products_data["product_id"] == product_id, 
                                             "reviews_last_month"].values[0]

    if reviews_last_month == 0:
        if reviews_this_month != 0:
            log.info(f"Last month reviews is 0 for product_id {product_id}, there is a 100% review growth")
            return 1    
        else :
            log.info(f"No review growth for product_id {product_id}")
            return 0
    review_growth = (reviews_this_month - reviews_last_month) / reviews_last_month

    return review_growth

def compute_seller_density_score(product_id):
    """
    Computes the seller density score for a product
    """
    number_of_competitors = products_data.loc[products_data["product_id"] == product_id, 
                                                "number_of_competitors"].values[0]
    
    if number_of_competitors == 0:
        return 1

    seller_density_score = 1 / log(number_of_competitors + 1)

    return seller_density_score

def compute_review_saturation_score(product_id):
    """
    Computes the review saturation score for a product
    """
    avg_top_five_compititor_reviews = products_data.loc[products_data["product_id"] == product_id, 
                                                        "avg_top_five_compititor_reviews"].values[0]

    if avg_top_five_compititor_reviews == 0:
        return 1

    review_saturation_score = 1 / log(avg_top_five_compititor_reviews + 1)

    return review_saturation_score

def compute_price_war_score(product_id):
    """
    Computes the price war score for a product
    """
    avg_margin = products_data.loc[products_data["product_id"] == product_id, 
                                    "avg_margin"].values[0]
    avg_selling_price = products_data.loc[products_data["product_id"] == product_id, 
                                        "avg_selling_price"].values[0]
    if avg_selling_price == 0:
        log.info(f"[WARNING] avg selling price is 0 for product_id {product_id}, this is not normal.")
        return 1
    price_war_score = avg_margin / avg_selling_price

    return price_war_score

def compute_delivery_time_score(product_id):
    """
    Computes the delivery time score for a product
    """
    delivery_time = products_data.loc[products_data["product_id"] == product_id, 
                                        "delivery_time"].values[0]

    if delivery_time == 0:
        return 1

    delivery_time_score = 1 / log(delivery_time + 1)

    return delivery_time_score

def compute_shipping_cost_score(product_id):
    """
    Computes the shipping cost score for a product
    """
    shipping_cost = products_data.loc[products_data["product_id"] == product_id, 
                                        "shipping_cost"].values[0]
    
    if shipping_cost == 0:
        return 1

    shipping_cost_score = 1 / log(shipping_cost + 1)

    return shipping_cost_score

def compute_size_weight_score(product_id):
    """
    Computes the size and weight score for a product
    """
    size = products_data.loc[products_data["product_id"] == product_id, 
                                        "size"].values[0]
    weight = products_data.loc[products_data["product_id"] == product_id, 
                                        "weight"].values[0]
    if size == 0 or weight == 0:
        log.info(f"[WARNING] size of weight is 0 for product_id {product_id}, this is not normal.")
        return 1
                                        
    size_weight_score = 1 / log(size * weight + 1 )

    return size_weight_score

def compute_fragility_score(product_id):
    """
    Computes the fragility score for a product
    """
    fragility = products_data.loc[products_data["product_id"] == product_id, 
                                    "fragility"].values[0]
    
    if fragility == 0:
        return 1

    fragility_score = 1 / log(fragility + 1)  

    return fragility_score

def compute_supplier_rating_score(product_id):
    """
    Computes the supplier rating score for a product
    """
    supplier_rating = products_data.loc[products_data["product_id"] == product_id, 
                                        "supplier_rating"].values[0]

    supplier_rating_score = supplier_rating / 5

    return supplier_rating_score

def compute_moq_score(product_id):
    """
    Computes the minimum order quantity score for a product
    """
    moq = products_data.loc[products_data["product_id"] == product_id, 
                            "moq"].values[0]
    if moq == 0:
        log.info(f"MOQ of supplier is 0 for product_id {product_id}, this is rare but perfect")
        return 1

    moq_score = 1 / log(moq + 1)

    return moq_score

def compute_supplier_response_rate_score(product_id):
    """
    Computes the supplier response rate score for a product
    """
    response_rate = products_data.loc[products_data["product_id"] == product_id, 
                                        "supplier_response_rate"].values[0]
    supplier_response_rate_score = response_rate / 100

    return supplier_response_rate_score

def compute_order_volume_score(product_id):
    """
    Computes the order volume score for a product
    """
    supplier_completed_orders = products_data.loc[products_data["product_id"] == product_id, 
                                    "supplier_completed_orders"].values[0]
    supplier_max_orders = products_data.loc[products_data["product_id"] == product_id, 
                                        "supplier_max_orders"].values[0]
    
    if supplier_max_orders == 0:
        log.info(f"Supplier has no orders so far for product_id {product_id}")
        return 0

    order_volume_score = log(supplier_completed_orders + 1) / log(supplier_max_orders + 1)

    return order_volume_score

def compute_trend_growth_score(product_id):
    """
    Computes the trend growth score for a product
    """
    current_tiktok_trend_score = products_data.loc[products_data["product_id"] == product_id, 
                                        "current_tiktok_trend_score"].values[0]
    last_month_tiktok_trend_score = products_data.loc[products_data["product_id"] == product_id,
                                        "last_month_tiktok_trend_score"].values[0] 

    if last_month_tiktok_trend_score == 0:
        if current_tiktok_trend_score != 0:
            log.info(f"Last month tiktok trend score is 0 for product_id {product_id}, there is 
            a 100% trend growth")
            return 1    
        else :
            log.info(f"No trend growth for product_id {product_id}")
            return 0     

    trend_growth_score = (current_tiktok_trend_score 
                         - last_month_tiktok_trend_score
                         ) / last_month_tiktok_trend_score

    return trend_growth_score

def compute_creator_adoption_score(product_id):
    """
    Computes the creator adoption score for a product
    """
    number_of_creators = products_data.loc[products_data["product_id"] == product_id, 
                                            "number_of_creators"].values[0]
    creator_adoption_score = log(number_of_creators + 1)

    return creator_adoption_score

def compute_rist_level(product_id):
    """
    Computes the risk level for a product

    Product Category	Compliance Risk	risk_level
    Phone accessories	Low	0.1
    Kitchen gadgets	    Low	0.1
    Cosmetics	        Medium/High	0.5
    Supplements	        High	0.9
    Medical devices	    Very high	1
    Batteries/electronicsMedium/High	0.8
    """
    #TODO : verify product categories in order to set the correct category names
    if product_category in ["Phone accessories", "Kitchen gadgets", "Korean lifestyle small goods",
                         "Korean pet accessories", "Korean desk & study accessories",
                         "Korean travel accessories"]:
        risk_level = 0.1
    elif product_category in ["Hair & scalp care tools", "Korean pet accessories"]:
        risk_level = 0.2
    elif product_category in ["K-beauty accessories"]:
        risk_level = 0.3
    elif product_category in ["Cosmetics"]:
        risk_level = 0.5
    elif product_category in ["Batteries/electronics", "Batteries", "Electronics"]:
        risk_level = 0.8
    elif product_category in ["Supplements"]:
        risk_level = 0.9
    elif product_category in ["Medical devices"]:
        risk_level = 1

    else : 
        log.info("WARNING: Product category not recognized, setting default risk level to 0.5")
        risk_level = 0.5

    return risk_level