# Product : 
A good product is :
- High demand 
- Low competition 
- Can we source it from korea ? is there korean suppliers ?
- Profitable : 
    selling price =  Product Cost 
                    + Domestic Shipping 
                    + Packaging 
                    + International Shipping 
                    + Shopee Fees 
                    + Payment Fees 
                    + Advertising Cost 
                    + Target profit
- Easy to market (explain)
- Scalable (stable supplier, acceptable delivery time, ...)

### Data sources : 
AliExpress, Shopee API, Shopify API, TikTok`

### AliExpress Data
Information we can get from AliExpress about products are : 
| Information                        | Available on AliExpress? | Useful For                          |
| ---------------------------------- | ------------------------ | ----------------------------------- |
| Product name/title                 | Yes                      | Product discovery                   |
| Product category                   | Yes                      | Product classification              |
| Product description                | Yes                      | Listing generation                  |
| Product images/videos              | Yes                      | Marketing assets                    |
| Product price                      | Yes                      | Pricing strategy                    |
| Discount price                     | Yes                      | Promotion analysis                  |
| Number of orders                   | Yes                      | Demand estimation                   |
| Product rating                     | Yes                      | Product quality scoring             |
| Number of reviews                  | Yes                      | Popularity estimation               |
| Review text                        | Yes                      | Sentiment analysis                  |
| Customer images in reviews         | Yes                      | Real-world product validation       |
| Shipping cost                      | Yes                      | Margin calculation                  |
| Shipping countries                 | Yes                      | Market targeting                    |
| Delivery time estimates            | Yes                      | Logistics evaluation                |
| Seller/store name                  | Yes                      | Supplier identification             |
| Seller/store rating                | Yes                      | Supplier scoring                    |
| Seller/store followers             | Yes                      | Supplier credibility                |
| Product variants (size/color/etc.) | Yes                      | Inventory planning                  |
| Related/recommended products       | Yes                      | Product graph/recommendation engine |
| Wishlist count (sometimes)         | Partially                | Trend estimation                    |
| MOQ                                | Usually No               | Better obtained from Alibaba        |
| Factory/manufacturer details       | Limited                  | Better obtained from Alibaba        |
| Production capacity                | No                       | Better obtained from Alibaba        |


### Example products: 
scalp massage brush, silicone facial cleansing pad, makeup puff, cosmetic spatula, cosmetic organizer, travel cosmetic bottle, shower scalp brush, hair towel, compact comb, brush holder. desk organizer, cute stationery, travel pouch, kitchen small tool, 
storage case. 



### Product table
CREATE TABLE products ( 
    id SERIAL PRIMARY KEY, 
    product_name TEXT (we have it), 
    supplier_name TEXT,
    category TEXT (we have it), 
    target_country TEXT (we have it), 
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
We added supplier_name to crate a relation between table products and table suppliers

### Product scoring formula: 
```
product_score = 0.25*demand_growth 
                + 0.2*low_competition 
                + 0.2*expected_margin 
                + 0.1*logistics_simplicity 
                + 0.1*supplier_reliability 
                + 0.1*tiktok_virality 
                + 0.05*compliance_safety
```

1. demand_growth formula:

`demand_growth = 0.5*OrderGrowth + 0.3*SearchTrendGrowth + 0.2*ReviewGrowth`

**where** `OrderGrowth = OrderGrowth_of_one_month = (OrderThisMonth - OrderLastMonth)/OrderLastMonth * 100`

**and** `SearchTrendGrowth = SearchTrend_of_one_month = (SearchThisMonth - SearchLastMonth)/SearchLastMonth * 100`

**and** `ReviewGrowth = ReviewGrowth_of_one_month = (ReveiwThisMonth - ReviewLastMonth)/OrderLastMonth * 100`

**Other formulas to consider** `OrderGrowth = 0.5*ShortTermGrowth(30d) + 0.3*MidTermGrowth(90d) + 0.2LongTermGrowth(1y)`

**Note :** Get Order and Reviews from AliExpress, and Search from **Google Trend** particulary the trend score. 