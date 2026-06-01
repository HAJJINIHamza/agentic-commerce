import pandas as pd 
from agents.pricing_optimization.product_pricing import ProductSellingPriceAgent

data_test = pd.read_csv("data/test_product_iter_1.csv", sep=";")
product_pricing_agent = ProductSellingPriceAgent(data_test)
product_id = data_test["id"].iloc[0]


if __name__ == "__main__":
    #FOR TESTING RUN FOLLOWING COMMAND
    # python -m tests.agents_testing.product_pricing_test
    selling_price = product_pricing_agent.get_product_selling_price(product_id)
    print ("Selling price should be : ", selling_price)

    simulated_selling_price = input("Enter a selling price to simulate profit and margin >> ")
    simulated_selling_price = float(simulated_selling_price)
    profit, margin = product_pricing_agent.simulate_profit(product_id, 
                                                           simulated_selling_price=simulated_selling_price)
    print ("Profit will be : ", profit)
    print ("Margin will be : ", margin)

    simulate_margin = input("Enter a margin to simulate the required selling price >> ")
    simulate_margin = float(simulate_margin)
    selling_price_for_margin = product_pricing_agent.simulate_selling_price_given_margin(product_id, 
                                                                              margin=simulate_margin)
    print (f"Selling price to achieve margin {simulate_margin}  is : {selling_price_for_margin}")

