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