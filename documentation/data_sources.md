# Agentic commerce data sources 

| Platform | best for | URL | Can we get most needed data |
| --- | --- | --- | --- |
| AliExpress | Product discovery, product ratings, reviews, pricing, competition estimation, trending products |  https://ko.aliexpress.com/ | Partially. You can get supplier/product data, but many teams still use scraping for large-scale extraction |
| Alibaba | Supplier information, MOQ, wholesale pricing, supplier verification, manufacturing details | https://www.alibaba.com/ | Partially. Basic product data is accessible, but large-scale market intelligence usually requires scraping |
| Shopee | Competitor analysis, local selling prices, product popularity, market validation in your target marketplace | https://shopee.com/ | Limited through API alone. Sales/market intelligence data often requires scraping because public competitor data is not fully exposed |

### Other plateforms but less restricted :
| Platform | Advantages | Api restrictions |
| --- | --- | --- |
| RapidAPI | Marketplace of APIs including ecommerce, product, pricing, and supplier-related APIs. Easier access than many official marketplace APIs | Low to medium. Usually simple signup + paid tier | 
| SerpiApi | Provides structured search/scraping APIs for Google Shopping, ecommerce sites, and marketplace data without handling anti-bot systems yourself | Low. Easy API access with usage-based pricing |

**Note :** Shopify is primarily an ecommerce infrastructure platform, not a product/supplier intelligence platform, it is not a convenient data source for our project


### Product Table Schema

CREATE TABLE products ( 
    id SERIAL PRIMARY KEY, 
    product_name TEXT, 
    category TEXT, 
    target_country TEXT, 
    demand_growth FLOAT, 
    competition_score FLOAT, 
    expected_margin FLOAT, 
    logistics_score FLOAT,  
    supplier_score FLOAT, 
    tiktok_score FLOAT, 
    compliance_score FLOAT, 
    total_score FLOAT, 
    status TEXT 
);


### Supplier Table Schema

CREATE TABLE suppliers ( 
    id SERIAL PRIMARY KEY, 
    company_name TEXT, 
    product_category TEXT, 
    unit_cost_krw FLOAT, 
    moq INTEGER, 
    lead_time_days INTEGER, 
    contact_email TEXT, 
    brand_authorization BOOLEAN, 
    export_ready BOOLEAN, 
    risk_score FLOAT 
); 

### ITER 1 DATA SOURCES FOR PRODUCT DATASET
- Shopee : https://shopee.sg/search?keyword=portable%20detangling%20brush&noCorrection=true&page=0
- TradeKorea : https://www.tradekorea.com/product/detail/P539583/Penguin-Clip.html
- AliBaba : https://www.alibaba.com/search/page?spm=a2700.prosearch.the-new-header_fy23_pc_search_bar.searchButton&SearchScene=proSearch&SearchText=portable+detangling+brush&pro=true&from=pcHomeContent
- TikTok Hashtags : https://tiktokhashtags.com/hashtag/siliconemask/
- TikTok platform : https://www.tiktok.com/tag/siliconemask
- Accio B2B chatbot : https://www.accio.com/c/48386737-9c73-46dc-afde-084878281543