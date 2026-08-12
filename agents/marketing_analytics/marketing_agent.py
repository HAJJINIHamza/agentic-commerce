import pandas as pd

from src.logger import get_logger

logger = get_logger(__name__)

class MarketingAgent:
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
        cpc = shopee_ads_data["Expense"]/shopee_ads_data["Clicks"]
        cr = shopee_ads_data["Orders"]/shopee_ads_data["Clicks"]
        if shopee_ads_data["Clicks"] != 0:
            number_of_impressions_needed = shopee_ads_data["Clicks"]/shopee_ads_data["CTR"]
        if shopee_ads_data["orders"] != 0:
            number_of_clicks_needed = shopee_ads_data["orders"]/shopee_ads_data["cr"]
        

        return cpc, cr, 

