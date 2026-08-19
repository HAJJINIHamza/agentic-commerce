import pandas as pd
from pathlib import Path

from src.logger import get_logger

logger = get_logger(__name__)

#SHOPEE ADS DATA COLUMNS : 
#Index(['User Name', 'Shop Name', 'Shop ID', 'Report Creation Time',
#       'Date Period', 'Sequence', 'Ad Name', 'Status', 'Ads Type',
#       'Product ID', 'Creative', 'Bidding Method', 'Placement', 'Start Date',
#       'End Date', 'Impression', 'Clicks', 'CTR', 'Add to Cart',
#       'Add to Cart Rate', 'Conversions', 'Direct Conversions',
#       'Conversion Rate', 'Direct Conversion Rate', 'Cost per Conversion',
#       'Cost per Direct Conversion', 'Items Sold', 'Direct Items Sold', 'GMV',
#       'Direct GMV', 'Expense', 'ROAS', 'Direct ROAS', 'ACOS', 'Direct ACOS',
#       'Product Impressions', 'Product Clicks', 'Product CTR',
#       'Voucher Amount', 'Vouchered Sales']

class marketingAgent:
    def __init__(self):
        pass

    def read_shopee_ads_data(self, file_path):
        """
        Read Shopee Ads data from a CSV file and return a DataFrame

        file_path : str : example : "data/marketing/shopee_ads/Shopee-Ads-Overall-Data-05_08_2026-11_08_2026.csv"
        """
        shopee_ads_head_info = pd.read_csv(file_path, nrows=5)

        shopee_ads_head_info = shopee_ads_head_info.T
        shopee_ads_head_info.reset_index(inplace=True, drop=True)

        shopee_ads_data = pd.read_csv(file_path, header=6 )

        shopee_ads_data_final = shopee_ads_data.copy()

        for col in shopee_ads_head_info:
            shopee_ads_data_final[col] = shopee_ads_head_info[col].values[0]

        #print ("Shopee_ads_head_info columns :", shopee_ads_head_info.columns)
        #print ("Shopee_ads_data columns :", shopee_ads_data.columns)

        final_columns = list(shopee_ads_head_info.columns) + list(shopee_ads_data.columns)

        shopee_ads_data_final = shopee_ads_data_final[final_columns]

        logger.info(f"Shopee Ads data read from {file_path}  successfully.")
        return shopee_ads_data_final

    def compute_overall_marketing_metrics(self, data):
        """
        Compute marketing metrics from Shopee Ads data
        """
        #data = data[data["Status"] == "Ongoing"]
        expense = float(data["Expense"].values[0])
        clicks = int(data["Clicks"].values[0])
        cpc = expense/clicks if clicks != 0 else 0
        conversions = int(data["Conversions"].values[0])
        conversion_rate = (conversions/clicks)*100 if clicks != 0 else 0
        impressions = float(data["Impression"].values[0])
        ctr = (clicks / impressions)*100 if impressions != 0 else 0
        roas = conversions / expense if expense != 0 else 0

        number_of_impressions_needed = round(100/ctr) if ctr != 0 else 0 #100 for percentage (1/ctr  * 100)

        number_of_clicks_needed = round(100/conversion_rate) if conversion_rate != 0 else 0

        marketing_metrics = {
                #"date_period" : data["Date Period"].values[0],
                #"ad_name": data["Ad Name"].values[0],
                "ctr_%": ctr,
                "cpc_$": cpc,
                "conversion_rate_%": conversion_rate,
                "roas_$": roas,
                "number_of_impressions_needed": number_of_impressions_needed,
                "number_of_clicks_needed": number_of_clicks_needed
                }
        
        return marketing_metrics

    def process_overall_data(self, data):
        """
        Process overall data and return data ready for dashboarding
        """

        marketing_metrics_columns =  ['Impression', 'Clicks', 'Add to Cart', 'Conversions', 'Direct Conversions', 
                                        'Items Sold', 'Direct Items Sold', 'GMV', 'Expense', 'Product Impressions', 
                                        'Product Clicks', 'Voucher Amount', 'Vouchered Sales']
        shopee_ads_date_details_columns = ['Start Date', 'End Date' ]
        shopee_ads_details_columns = ['User Name', 'Shop Name', 'Shop ID', 'Report Creation Time',
                                        'Sequence', 'Ad Name', 'Status', 'Ads Type',
                                        'Product ID', 'Creative', 'Bidding Method', 'Placement']

        final_data = data[marketing_metrics_columns].agg(["sum"]).reset_index(drop=True)

        marketing_metrics = self.compute_overall_marketing_metrics(final_data)

        for key, value in marketing_metrics.items():
            final_data[key] = value

        final_data = pd.concat([data[shopee_ads_details_columns].head(1), final_data], axis = 1)

        start_date = data[shopee_ads_date_details_columns]["Start Date"].min()
        end_date = data[shopee_ads_date_details_columns]["End Date"].max()

        final_data["start_date"] = start_date
        final_data["end_date"] = end_date

        return final_data
        

    def add_new_marketing_mertrics_to_data(self, data):
        """
        Adds new markeing metrics like cpc, number of impressions needed to data
        return data with added metrics
        """

        data["ctr_%"] = data["CTR"].apply(lambda x: float(x.replace("%", "")))
        data["cpc_$"] = data["Expense"]/data["Clicks"]
        data["cr"] = data["Conversion Rate"].apply(lambda x:float(x.replace("%", "")))
        data["number_of_impressions_needed"] = data["ctr_%"].apply(lambda x: round(100/x) if x!=0 else 0)
        data["number_of_clicks_needed"] = data["cr"].apply(lambda x: round(100/x) if x!=0 else 0)

        logger.info("Added new marketing metrics to data")

        return data

    def process_day_by_day_data(self, start_day = 5, end_day=13):
        """
        Process Shopee Ads data to create a day-by-day DataFrame

        Params:
        ------
        start_day : 5, 9, 12, ...
        end_day : 5, 9, 12, ...

        """
        end_day_data_path = Path(f"data/marketing/shopee_ads/day_by_data_data/Shopee-Ads-Overall-Data-{end_day:02d}_08_2026-{end_day:02d}_08_2026.csv")
        if not end_day_data_path.exists():
            raise ValueError(f"File {end_day_data_path} doesn's exist, End day {end_day} is out of range.")

        overall_data = []
        for day in range(start_day, end_day + 1):
            file_path = f"data/marketing/shopee_ads/day_by_data_data/Shopee-Ads-Overall-Data-{day:02d}_08_2026-{day:02d}_08_2026.csv"
            day_data = self.read_shopee_ads_data(file_path)
            day_data = day_data[day_data.index == 0]
            overall_data.append(day_data)

        overall_data = pd.concat(overall_data)

        overall_data["start_date"] = overall_data["Date Period"].apply(lambda x: x.split(" - ")[0])
        overall_data["end_date"] = overall_data["Date Period"].apply(lambda x: x.split(" - ")[1])

        overall_data = self.add_new_marketing_mertrics_to_data(overall_data)

        logger.info("Processed day by day data successfully")

        return overall_data


"""
if __name__ == "__main__":
    file_path = "data/marketing/shopee_ads/overall_data/Shopee-Ads-Overall-Data-05_08_2026-12_08_2026.csv"
    marketing_agent = marketingAgent()
    #shopee_ads_data = marketing_agent.read_shopee_ads_data(file_path)
    #shopee_ads_data_processed = marketing_agent.process_overall_data(shopee_ads_data)
    #marketing_metrics = marketing_agent.compute_marketing_metrics(shopee_ads_data)
    overall_data = marketing_agent.process_day_by_day_data(5, 12)
    print (overall_data)
"""

