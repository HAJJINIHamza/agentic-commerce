import pandas as pd 
from agents.pricing_optimization.product_pricing import ProductSellingPriceAgent

def test_get_product_selling_price():
    data_test = pd.read_csv("data/test_product_iter_1.csv", sep=";")
    product_pricing_agent = ProductSellingPriceAgent(data_test)
    product_id = data_test["id"].iloc[0]
    selling_price = product_pricing_agent.get_product_selling_price(product_id)
    return selling_price

if __name__ == "__main__":
    #FOR TESTING RUN FOLLOWING COMMAND
    # python -m tests.agents_testing.product_pricing_test
    selling_price = test_get_product_selling_price()
    print ("Selling price : ", selling_price)