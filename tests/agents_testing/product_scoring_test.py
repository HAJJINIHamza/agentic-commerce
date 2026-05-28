import pandas as pd 
from src.logger import get_logger

from agents.products_scoring.product_scoring import score_product

log = get_logger(__name__)

def test_score_product():
    log.info("Testing score_product_function")
    data_test = pd.read_csv("data/test_product_iter_1.csv", sep=";")
    print ("data columns :", data_test.columns)
    product_id = data_test["id"].iloc[0]
    print ("Product id is : ", product_id)
    score = score_product(product_id)
    log.info(f"Score for product_id {product_id}: is {score}")
    return score

if __name__ == "__main__":
    #FOR TESTING RUN FOLLOWING COMMAND
    # python -m tests.agents_testing.product_scoring_test
    score = test_score_product()
    print ("Score : ", score)
