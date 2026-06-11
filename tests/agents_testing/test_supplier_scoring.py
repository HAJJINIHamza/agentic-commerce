import pandas as pd 
from agents.supplier_scoring.supplier_scoring import supplierScoringAgent

def test_supplier_scoring():
    supplier_data = pd.read_csv("data/test_supplier_iter_1.csv", sep=";")
    supplier_scoring_agent = supplierScoringAgent(supplier_data)
    supplier_id = supplier_data["supplier_id"].iloc[0]
    supplier_score, _ = supplier_scoring_agent.compute_supplier_score(supplier_id)
    return supplier_score

if __name__ == "__main__":
    supplier_score = test_supplier_scoring()
    print (f"Supplier_socre is : {supplier_score}")




