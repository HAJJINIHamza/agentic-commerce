import pandas as pd 
from src.logger import get_logger
from math import log

#logger
logger = get_logger(__name__)

#Read products level 3 data 
products_data = pd.read_csv("data/test_product_iter_1.csv", sep=";")
print(products_data.head())

#Make sure num columns are in numeric format
num_columns = [col for col in products_data.columns \
                if col not in ["id", "product_name", "product_category"]]

print ("Transforming num columns to numeric format")
products_data[num_columns] = (products_data[num_columns]
                              .replace(",", ".", regex=True)
                              .apply(pd.to_numeric, errors="coerce"))

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
    print ("Scoring product")
    demand_growth = compute_demand_growth(product_id)
    logger.info(f"Demand growth for product_id {product_id} is {demand_growth}")
    low_competition_score = compute_competition_score(product_id)
    logger.info(f"Low competition score for product_id {product_id} is {low_competition_score}")
    expected_margin = compute_expected_margin(product_id)
    logger.info(f"Expected margin for product_id {product_id} is {expected_margin}")
    logistics_simplicity = compute_logistics_simplicity(product_id)
    logger.info(f"Logistics simplicity score for product_id {product_id} is {logistics_simplicity}")
    supplier_reliability = compute_supplier_reliability(product_id)
    logger.info(f"Supplier reliability score for product_id {product_id} is {supplier_reliability}")
    tiktok_virality = compute_tiktok_virality(product_id)
    logger.info(f"TikTok virality score for product_id {product_id} is {tiktok_virality}")
    compliance_safety = compute_compliance_safety(product_id)
    logger.info(f"Compliance and safety score for product_id {product_id} is {compliance_safety}")

    product_score = (0.25 * demand_growth 
                    + 0.2 * low_competition_score 
                    + 0.2 * expected_margin 
                    + 0.1 * logistics_simplicity 
                    + 0.1 * supplier_reliability 
                    + 0.1 * tiktok_virality 
                    + 0.05 * compliance_safety)

    logger.info(f"Computed product score for product_id {product_id}: {product_score}")
    return product_score

# Level 1 metrics

def compute_demand_growth(product_id):
    """
    Computes the demand growth for a product
    """
    print ("Computing demand growth")
    order_growth = compute_order_growth(product_id)
    search_trend_growth = compute_search_trend_growth(product_id)
    review_growth = compute_review_growth(product_id)

    demand_growth = (0.5 * order_growth 
                    + 0.3 * search_trend_growth
                    + 0.2 * review_growth)

    print (f"demand_growth is : {demand_growth}")
    return demand_growth

def compute_competition_score(product_id):
    """
    Computes the low competition score for a product
    """
    print("Computing low competition score")
    seller_density_score = compute_seller_density_score(product_id)
    review_saturation_score = compute_review_saturation_score(product_id)
    price_war_score = compute_price_war_score(product_id)

    low_competition_score = (0.5 * seller_density_score 
                         + 0.3 * review_saturation_score  
                         + 0.2 * price_war_score)
    print (f"low_competition_score is : {low_competition_score}")
    return low_competition_score

def compute_expected_margin(product_id):
    """
    Computes the expected margin for a product
    """
    print("Computing expected margin")
    selling_price = products_data.loc[products_data["id"] == product_id, 
                                        "avg_selling_price"].values[0]
    product_cost = products_data.loc[products_data["id"] == product_id, 
                                        "product_cost"].values[0]
    shipping_cost = products_data.loc[products_data["id"] == product_id,    
                                        "shipping_cost"].values[0]
    platform_fees = products_data.loc[products_data["id"] == product_id, 
                                        "platform_fees"].values[0]
    advertising_costs = products_data.loc[products_data["id"] == product_id, 
                                        "advertising_costs"].values[0]

    expected_margin = (selling_price
                       - product_cost
                       - shipping_cost
                       - platform_fees
                       - advertising_costs
                       ) / selling_price
    print (f"expected_margin is : {expected_margin}")
    return expected_margin

def compute_logistics_simplicity(product_id):
    """
    Computes the logistics simplicity score for a product
    """
    print ("Computing logistics simplicity score")
    delivery_time_score = compute_delivery_time_score(product_id)
    shipping_cost_score = compute_shipping_cost_score(product_id)
    weight_score = compute_size_weight_score(product_id)
    #TODO : Think about adding fragility score later
    #fragility_score = compute_fragility_score(product_id)

    logistics_simplicity_score = (0.4 * delivery_time_score 
                                + 0.3 * shipping_cost_score 
                                + 0.2 * weight_score 
                                )

    print (f"logistics_simplicity_score is : {logistics_simplicity_score}")
    return logistics_simplicity_score

def compute_supplier_reliability(product_id):
    """
    Computes the supplier reliability score for a product
    """
    print ("Computing supplier reliability score")
    supplier_rating_score = compute_supplier_rating_score(product_id)
    moq_score = compute_moq_score(product_id)
    supplier_response_rate_score = compute_supplier_response_rate_score(product_id)
    order_volume_score = compute_order_volume_score(product_id)

    supplier_reliability_score = (0.3 * supplier_rating_score + 
                                 0.3 * moq_score + 
                                 0.2 * supplier_response_rate_score + 
                                 0.2 * order_volume_score)
    print (f"supplier_reliability_score is : {supplier_reliability_score}")
    return supplier_reliability_score

def compute_tiktok_virality(product_id):
    """
    Computes the TikTok virality score for a product
    """
    print ("Computing TikTok virality score")
    trend_growth_score = compute_trend_growth_score(product_id)
    creator_adoption_score = compute_creator_adoption_score(product_id)

    tiktok_virality_score = (0.6 * trend_growth_score + 
                            0.4 * creator_adoption_score)
    print (f"tiktok_virality_score is : {tiktok_virality_score}")
    return tiktok_virality_score

def compute_compliance_safety(product_id):
    """
    Computes the compliance and safety score for a product
    """
    print ("Computing compliance and safety score")
    risk_level = compute_risk_level(product_id)

    compliance_safety_score = 1 - risk_level 
    print (f"compliance_safety_score is : {compliance_safety_score}")
    return compliance_safety_score


#Level 2 metrics 

def compute_order_growth(product_id):
    """
    Computes the order growth for a product
    """
    print ("Computing order growth")
    order_this_month = products_data.loc[products_data["id"] == product_id, 
                                        "orders_this_month"].values[0]
    order_last_month = products_data.loc[products_data["id"] == product_id, 
                                        "orders_last_month"].values[0]
    
    if order_last_month == 0:
        if order_this_month != 0:
            logger.info(f"Last month orders is 0 for product_id {product_id}, there is a 100% order growth")
            return 1    
        else :
            logger.info(f"No order growth for product_id {product_id}")
            return 0

    order_growth = (order_this_month - order_last_month) / order_last_month 
    print (f"order_growth is : {order_growth}")
    return order_growth

def compute_search_trend_growth(product_id):
    """
    Computes the search trend growth for a product
    """
    print ("Computing search trend growth")
    search_this_month = products_data.loc[products_data["id"] == product_id, 
                                        "search_this_month"].values[0]
    search_last_month = products_data.loc[products_data["id"] == product_id, 
                                        "search_last_month"].values[0]
    
    if search_last_month == 0:
        if search_this_month != 0:
            logger.info(f"Last month search is 0 for product_id {product_id}, there is a 100% search trend growth")
            return 1    
        else :
            logger.info(f"No search trend growth for product_id {product_id}")
            return 0

    search_trend_growth = (search_this_month - search_last_month) / search_last_month

    print (f"search_trend_growth is : {search_trend_growth}")
    return search_trend_growth

def compute_review_growth(product_id):
    """
    Computes the review growth for a product
    """
    print ("Computing review growth")
    reviews_this_month = products_data.loc[products_data["id"] == product_id, 
                                             "reviews_this_month"].values[0]
    reviews_last_month = products_data.loc[products_data["id"] == product_id, 
                                             "reviews_last_month"].values[0]

    if reviews_last_month == 0:
        if reviews_this_month != 0:
            logger.info(f"Last month reviews is 0 for product_id {product_id}, there is a 100% review growth")
            return 1    
        else :
            logger.info(f"No review growth for product_id {product_id}")
            return 0
    review_growth = (reviews_this_month - reviews_last_month) / reviews_last_month
    print (f"review_growth is : {review_growth}")
    return review_growth

def compute_seller_density_score(product_id):
    """
    Computes the seller density score for a product
    """
    print ("Computing seller density score")
    number_of_competitors = products_data.loc[products_data["id"] == product_id, 
                                                "number_of_competitors"].values[0]
    
    if number_of_competitors == 0:
        return 1

    seller_density_score = 1 / log(number_of_competitors + 1)

    print (f"seller_density_score is : {seller_density_score}")
    return seller_density_score

def compute_review_saturation_score(product_id):
    """
    Computes the review saturation score for a product
    """
    print ("Computing review saturation score")
    avg_top_five_compititor_reviews = products_data.loc[products_data["id"] == product_id, 
                                                        "avg_top_five_competitor_reviews"].values[0]

    if avg_top_five_compititor_reviews == 0:
        return 1

    review_saturation_score = 1 / log(avg_top_five_compititor_reviews + 1)

    print (f"review_saturation_score is : {review_saturation_score}")
    return review_saturation_score

def compute_price_war_score(product_id):
    """
    Computes the price war score for a product
    """
    print ("Computing price war score")
    avg_margin = products_data.loc[products_data["id"] == product_id, 
                                    "avg_margin"].values[0]
    avg_selling_price = products_data.loc[products_data["id"] == product_id, 
                                        "avg_selling_price"].values[0]

    if avg_selling_price == 0:
        logger.info(f"[WARNING] avg selling price is 0 for product_id {product_id}, this is not normal.")
        return 1
    print (f"avg_margin is : {avg_margin}")
    print (f"avg_selling_price is : {avg_selling_price}")
    price_war_score = avg_margin / avg_selling_price
    print (f"price_war_score is : {price_war_score}")
    return price_war_score

def compute_delivery_time_score(product_id):
    """
    Computes the delivery time score for a product
    """
    print ("Computing delivery time score")
    delivery_time = products_data.loc[products_data["id"] == product_id, 
                                        "delivery_time"].values[0]

    if delivery_time == 0:
        return 1

    delivery_time_score = 1 / log(delivery_time + 1)
    print (f"delivery_time_score is : {delivery_time_score}")
    return delivery_time_score

def compute_shipping_cost_score(product_id):
    """
    Computes the shipping cost score for a product
    """
    print ("Computing shipping cost score")
    shipping_cost = products_data.loc[products_data["id"] == product_id, 
                                        "shipping_cost"].values[0]
    
    if shipping_cost == 0:
        return 1

    shipping_cost_score = 1 / log(shipping_cost + 1)
    print (f"shipping_cost_score is : {shipping_cost_score}")
    return shipping_cost_score

def compute_size_weight_score(product_id):
    """
    Computes the size and weight score for a product
    """
    print ("Computing size and weight score")
    size = products_data.loc[products_data["id"] == product_id, 
                                        "size"].values[0]
    weight = products_data.loc[products_data["id"] == product_id, 
                                        "weight"].values[0]
    if size == 0 or weight == 0:
        logger.info(f"[WARNING] size or weight is 0 for product_id {product_id}, this is not normal.")
        return 1
                                        
    size_weight_score = 1 / log(size * weight + 1 )

    print (f"size_weight_score is : {size_weight_score}")
    return size_weight_score

def compute_fragility_score(product_id):
    """
    Computes the fragility score for a product
    """
    print ("Computing fragility score")
    fragility = products_data.loc[products_data["id"] == product_id, 
                                    "fragility"].values[0]
    
    if fragility == 0:
        return 1

    fragility_score = 1 / log(fragility + 1)  

    print (f"fragility_score is : {fragility_score}")
    return fragility_score

def compute_supplier_rating_score(product_id):
    """
    Computes the supplier rating score for a product
    """
    print ("Computing supplier rating score")
    supplier_rating = products_data.loc[products_data["id"] == product_id, 
                                        "supplier_rating"].values[0]

    supplier_rating_score = supplier_rating / 5
    print ("supplier_rating_score is : ", supplier_rating_score)
    return supplier_rating_score

def compute_moq_score(product_id):
    """
    Computes the minimum order quantity score for a product
    """
    print ("Computing MOQ score")
    moq = products_data.loc[products_data["id"] == product_id, 
                            "moq"].values[0]
    if moq == 0:
        logger.info(f"MOQ of supplier is 0 for product_id {product_id}, this is rare but perfect")
        return 1

    moq_score = 1 / log(moq + 1)
    print (f"moq_score is : {moq_score}")
    return moq_score

def compute_supplier_response_rate_score(product_id):
    """
    Computes the supplier response rate score for a product
    """
    print ("Computing supplier response rate score")
    response_rate = products_data.loc[products_data["id"] == product_id, 
                                        "supplier_response_rate"].values[0]
    supplier_response_rate_score = response_rate / 100

    print (f"supplier response rate score is : {supplier_response_rate_score}")

    return supplier_response_rate_score

def compute_order_volume_score(product_id):
    """
    Computes the order volume score for a product
    """
    print ("Computing order volume score")
    supplier_completed_orders = products_data.loc[products_data["id"] == product_id, 
                                    "supplier_completed_orders"].values[0]
    supplier_max_orders = products_data.loc[products_data["id"] == product_id, 
                                        "supplier_max_orders"].values[0]

    if supplier_max_orders == 0:
        logger.info(f"Supplier has no orders so far for product_id {product_id}")
        return 0

    order_volume_score = log(supplier_completed_orders + 1) / log(supplier_max_orders + 1)

    print (f"order volume score is : {order_volume_score}")
    return order_volume_score

def compute_trend_growth_score(product_id):
    """
    Computes the trend growth score for a product
    """
    print ("Computing trend growth score")
    current_tiktok_trend_score = products_data.loc[products_data["id"] == product_id, 
                                        "current_tiktok_trend_score"].values[0]
    last_month_tiktok_trend_score = products_data.loc[products_data["id"] == product_id,
                                        "last_month_tiktok_trend_score"].values[0] 

    if last_month_tiktok_trend_score == 0:
        if current_tiktok_trend_score != 0:
            logger.info(f"Last month tiktok trend score is 0 for product_id {product_id}, there is a 100% trend growth")
            return 1    
        else :
            logger.info(f"No trend growth for product_id {product_id}")
            return 0     

    trend_growth_score = (current_tiktok_trend_score 
                         - last_month_tiktok_trend_score
                         ) / last_month_tiktok_trend_score

    print (f"trend_growth_score is : {trend_growth_score}")

    return trend_growth_score

def compute_creator_adoption_score(product_id):
    """
    Computes the creator adoption score for a product
    """
    print ("Computing creator adoption score")
    number_of_creators = products_data.loc[products_data["id"] == product_id, 
                                            "number_of_creators"].values[0]
    creator_adoption_score = log(number_of_creators + 1)

    print (f"number of creators is {number_of_creators}")

    return creator_adoption_score

def compute_risk_level(product_id):
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
    print ("Computing risk level")

    product_category = products_data.loc[products_data["id"] == product_id, 
                                         "product_category"].values[0]

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
        logger.info("WARNING: Product category not recognized, setting default risk level to 0.5")
        risk_level = 0.5
    
    print(f"risk level is : {risk_level}")

    return risk_level