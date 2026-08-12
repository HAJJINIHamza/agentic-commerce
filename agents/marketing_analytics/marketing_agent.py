import pandas as pd

from src.logger import get_logger

logger = get_logger(__name__)

class marketingAgent:
    def __init__(self):
        pass

    def read_shopee_ads_data(self, file_path):
        """
        Read Shopee Ads data from a CSV file and return a DataFrame

        file_path : str : example : "data/marketing/shopee_ads/Shopee-Ads-Overall-Data-05_08_2026-11_08_2026.csv"
        """
        shopee_ads_head_info = pd.read_csv(file_path, nrows=5)
        shopee_ads_head_info

        shopee_ads_head_info = shopee_ads_head_info.T
        shopee_ads_head_info.reset_index(inplace=True, drop=True)

        shopee_ads_head_info = pd.concat([shopee_ads_head_info, shopee_ads_head_info], axis=0).reset_index(drop=True)
        shopee_ads_head_info

        shopee_ads_data = pd.read_csv(file_path, header=6 )
        shopee_ads_data

        shopee_ads_data_final = pd.concat([shopee_ads_head_info, shopee_ads_data], axis=1)
        logger.info(f"Shopee Ads data read from {file_path}  successfully.")
        return shopee_ads_data_final
    
    def compute_marketing_metrics(self, shopee_ads_data):
        """
        Compute marketing metrics from Shopee Ads data
        """
        shopee_ads_data = shopee_ads_data[shopee_ads_data["Status"] == "Ongoing"]
        expense = float(shopee_ads_data["Expense"].values[0])
        clicks = int(shopee_ads_data["Clicks"].values[0])
        cpc = expense/clicks if clicks != 0 else None
        conversions = int(shopee_ads_data["Conversions"].values[0])
        conversion_rate = float(shopee_ads_data["Conversion Rate"].values[0].replace("%", ""))
        ctr = float(shopee_ads_data["CTR"].values[0].replace("%", ""))

        number_of_impressions_needed = 100/ctr if ctr != 0 else None #100 for percentage (1/ctr  * 100)

        number_of_clicks_needed = 100/conversion_rate if conversion_rate != 0 else None

        marketing_metrics = {
                "date_period" : shopee_ads_data["Date Period"].values[0],
                "ad_name": shopee_ads_data["Ad Name"].values[0],
                "ctr_%": ctr,
                "cpc_$": cpc,
                "conversion_rate_%": conversion_rate,
                "number_of_impressions_needed": number_of_impressions_needed,
                "number_of_clicks_needed": number_of_clicks_needed
                }
        
        logger.info(f"Marketing metrics : {marketing_metrics}")

        return marketing_metrics

if __name__ == "__main__":
    file_path = "data/marketing/shopee_ads/Shopee-Ads-Overall-Data-05_08_2026-11_08_2026.csv"
    marketing_agent = marketingAgent()
    shopee_ads_data = marketing_agent.read_shopee_ads_data(file_path)
    marketing_metrics = marketing_agent.compute_marketing_metrics(shopee_ads_data)
    print (marketing_metrics)


