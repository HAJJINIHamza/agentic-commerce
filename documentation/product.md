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
                + 0.2*low_competition_score
                + 0.2*expected_margin 
                + 0.1*logistics_simplicity 
                + 0.1*supplier_reliability 
                + 0.1*tiktok_virality 
                + 0.05*compliance_safety
```

1. demand_growth formula:
```
demand_growth = 0.5*OrderGrowth 
                + 0.3*SearchTrendGrowth 
                + 0.2*ReviewGrowth
```

**where** `OrderGrowth = OrderGrowth_of_one_month = (OrderThisMonth - OrderLastMonth)/OrderLastMonth`

**and** `SearchTrendGrowth = SearchTrend_of_one_month = (SearchThisMonth - SearchLastMonth)/SearchLastMonth`

**and** `ReviewGrowth = ReviewGrowth_of_one_month = (ReveiwThisMonth - ReviewLastMonth)/OrderLastMonth`

**Other formulas to consider** `OrderGrowth = 0.5*ShortTermGrowth(30d) + 0.3*MidTermGrowth(90d) + 0.2LongTermGrowth(1y)`

**Note :** Get Order and Reviews from AliExpress, and Search from **Google Trend** particulary the trend score. 

2. Low_competition formula :
```
LowCompetitionScore =
    0.5 * SellerDensityScore +
    0.3 * ReviewSaturationScore +
    0.2 * PriceWarScore
```

| Component             | Meaning                                                       | Formula               | Possible Source | 
| --- |--- |---|---|
| SellerDensityScore    | Number of sellers offering similar products                   | SellerDensityScore = 1 / log(NumberOfCompetitors + 1)                       | [Shopee](https://shopee.com?utm_source=chatgpt.com) / [Coupang](https://www.coupang.com?utm_source=chatgpt.com)              |
| ReviewSaturationScore | Whether top competitors already have massive review counts    | ReviewSaturationScore = 1 / log(AvgTop5CompetitorReviews + 1)                      | [AliExpress](https://www.aliexpress.com?utm_source=chatgpt.com)                                                              |
| PriceWarScore         | How compressed margins are due to intense pricing competition |PriceWarScore = AvgMargin / AvgSellingPrice                        | Marketplace pricing data              |

> High low_competition_score means that competition is low, means product is good, low low_competition_score means competition is high therefore do not consider this product

3. expected_margin formula:
```
ExpectedMargin =(SellingPrice
                - ProductCost
                - ShippingCost
                - PlatformFees
                - AdvertisingCost)
                / SellingPrice
```

**Note:** For later iterations add Payment fees and packaging costs, for now they are not a major contributors. 

4. logistics_simplicity formula:
```
LogisticsSimplicityScore = 0.4 * DeliveryTimeScore +
                            0.3 * ShippingCostScore +
                            0.2 * SizeWeightScore +
                            0.1 * FragilityScore
```

|Componenet|formula|
| --- | --- |
|DeliveryTimeScore|1/DeliveryTime|
|ShippingCostScore|1/ShippingCost|
|SizeWeightScore|1/log(size*weight+1)|
|FragilityScore|1/log(Fragility+1)|

5. supplier_reliability formula : 
```
SupplierReliabilityScore = 0.3 * SupplierRatingScore +
                            0.3 * MoqScore +
                            0.2 * ResponseRateScore +
                            0.2 * OrderVolumeScore
```

|Component|Formula|explination
| --- | --- | --- |
|SupplierRatingScore | supplier_rating/5| rating of supplier |
|MoqScore |1/log(MOQ + 1)| can we test with minimum quantity |
|ResponseRateScore|ResponseRate/100| Supplier should answer fast |
|OrderVolumeScore| log(CompletedOrders + 1)/ log(MaxOrders)| Nmbr of completed orders |

> MOQ stands for Minimum Order Quantity. It is the smallest number of units a supplier is willing to manufacture or sell in a single order, lower is better. 

**Note :** Supplier informations are better to get from AliBaba

6. tiktok_virality score: 
``` 
TikTokViralityScore =
    0.6 * TrendGrowthScore +
    0.4* CreatorAdoptionScore +
```

|Componenet|Formula|
|---|---|
|TrendGrowthScore|(CurrentTrendScore - LastMonthTrendScore)/LastMonthTrendScore |
|CreatorAdoptionScore|log(NumberOfCreators + 1)|

**Note :** you can add  EngagementScore = log(TotalEngagement + 1) to the formula

**Note :** Get Tiktok data from TikTok Creative Center

7. compliance_safety formula :

``` 
compliance_safety_score = 1 - risk_level 
```

| Product Category      | Compliance Risk | risk_level |
| --------------------- | --------------- | -----------|
| Phone accessories     | Low             | 0.1        |
| Kitchen gadgets       | Low             | 0.1        |
| Cosmetics             | Medium/High     | 0.5        |
| Supplements           | High            | 0.9        |
| Medical devices       | Very high       | 1          |
| Batteries/electronics | Medium/High     | 0.8        |

### Product pricing formula
- Formula 1 
```
Selling Price = Product Cost 
                + Domestic Shipping 
                + Packaging 
                + International Shipping 
                + Shopee Fees 
                + Payment Fees 
                + Advertising Cost  
                + Target Profit 
```
- Formula 2 :
```
selling_price = fixed_cost / (1 - total_rate) 
```

Where

```
fixed_cost = Product Cost 
            + Domestic Shipping 
            + Packaging 
            + International Shipping 
            + Plateform Fees 
            + Payment Fees 
            + Advertising Cost  
```
```
total_rate = commission_rate 
            + transaction_fee_rate 
            + payoneer_fee_rate 
            + service_fee_rate 
            + ad_cost_rate 
            + target_margin_rate 
```

Where :
total_rate is the target profit margin, which means the percentage of profit we are willing to make from the selling price.
Example total rate : 0.3, 0.492
Example componenets of total rate:

| Component         | Rate |
| ----------------- | ---- |
| Shopee commission | 8%   |
| Transaction fee   | 3%   |
| Payoneer fee      | 2%   |
| Service fee       | 2%   |
| Ads               | 15%  |
| Target margin     | 20%  |

> in case it is hard to use the total rate formula, here is some estimations that could be used : 

| Category                     | Product Example               | Estimated Target Profit Margin |
| ---------------------------- | ----------------------------- | ------------------------------ |
| K-beauty accessories         | Scalp massage brush           | 35% – 50%                      |
| K-beauty accessories         | Silicone facial cleansing pad | 40% – 60%                      |
| K-beauty accessories         | Makeup puff                   | 45% – 65%                      |
| K-beauty accessories         | Cosmetic spatula              | 50% – 70%                      |
| K-beauty accessories         | Cosmetic organizer            | 30% – 45%                      |
| K-beauty accessories         | Travel cosmetic bottle        | 35% – 55%                      |
| Hair & scalp care tools      | Shower scalp brush            | 35% – 50%                      |
| Hair & scalp care tools      | Hair towel                    | 30% – 45%                      |
| Hair & scalp care tools      | Compact comb                  | 40% – 60%                      |
| Hair & scalp care tools      | Brush holder                  | 40% – 55%                      |
| Korean lifestyle small goods | Desk organizer                | 25% – 40%                      |
| Korean lifestyle small goods | Cute stationery               | 50% – 80%                      |
| Korean lifestyle small goods | Travel pouch                  | 35% – 55%                      |
| Korean lifestyle small goods | Kitchen small tool            | 30% – 50%                      |
| Korean lifestyle small goods | Storage case                  | 25% – 40%                      |

> In case we want to use the total_rate formula here is where you can find its components : 

| Component            | What It Represents                                                        | Where You Can Get It                                                                                                     |
| -------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Commission rate      | Marketplace commission taken on each sale                                 | [Shopee Seller Education Hub](https://seller.shopee.sg/edu/home?utm_source=chatgpt.com) or marketplace fee documentation |
| Transaction fee rate | Payment transaction processing fee charged by marketplace/payment gateway | Shopee fee documentation or payment provider docs                                                                        |
| Payoneer fee rate    | International withdrawal/conversion fee                                   | [Payoneer](https://www.payoneer.com?utm_source=chatgpt.com) pricing pages                                                |
| Service fee rate     | Miscellaneous marketplace operational/service fees                        | Marketplace seller fee pages                                                                                             |
| Ad cost rate         | Percentage of revenue spent on ads to acquire customers                   | Initially estimated manually, later computed from your historical ad campaigns                                           |
| Target margin rate   | Desired net profit percentage                                             | Business decision based on strategy/product category                                                                     |


### Product first list

| id | Category                        | Product Example                |
| ---| ------------------------------- | ------------------------------ |
| 1  | K-beauty accessories            | Scalp massage brush            |
| 2  | K-beauty accessories            | Silicone facial cleansing pad  |
| 3  | K-beauty accessories            | Makeup puff                    |
| 4  | K-beauty accessories            | Cosmetic spatula               |
| 5  | K-beauty accessories            | Cosmetic organizer             |
| 6  | K-beauty accessories            | Travel cosmetic bottle         |
| 7  | K-beauty accessories            | Ice face roller                |
| 8  | K-beauty accessories            | Reusable silicone mask cover   |
| 9  | K-beauty accessories            | Blackhead remover tool kit     |
| 10 | K-beauty accessories            | Mini skincare fridge organizer |
| 11 | Hair & scalp care tools         | Shower scalp brush             |
| 12 | Hair & scalp care tools         | Hair towel                     |
| 13 | Hair & scalp care tools         | Compact comb                   |
| 14 | Hair & scalp care tools         | Brush holder                   |
| 15 | Hair & scalp care tools         | Heatless hair curler           |
| 16 | Hair & scalp care tools         | Hair section clips             |
| 17 | Hair & scalp care tools         | Portable detangling brush      |
| 18 | Hair & scalp care tools         | Scalp oil applicator bottle    |
| 19 | Korean lifestyle small goods    | Desk organizer                 |
| 20 | Korean lifestyle small goods    | Cute stationery                |
| 21 | Korean lifestyle small goods    | Travel pouch                   |
| 22 | Korean lifestyle small goods    | Kitchen small tool             |
| 23 | Korean lifestyle small goods    | Storage case                   |
| 24 | Korean lifestyle small goods    | Cable organizer                |
| 25 | Korean lifestyle small goods    | Mini trash bin for desk        |
| 26 | Korean lifestyle small goods    | Reusable shopping bag          |
| 27 | Korean lifestyle small goods    | Foldable laundry basket        |
| 28 | Korean lifestyle small goods    | Refrigerator storage box       |
| 29 | Korean desk & study accessories | Laptop stand                   |
| 30 | Korean desk & study accessories | Keyboard cleaning gel          |
| 31 | Korean desk & study accessories | Monitor memo board             |
| 32 | Korean desk & study accessories | Aesthetic mouse pad            |
| 33 | Korean desk & study accessories | Tablet stand                   |
| 34 | Korean travel accessories       | Compression packing cubes      |
| 35 | Korean travel accessories       | Passport holder                |
| 36 | Korean travel accessories       | Portable jewelry case          |
| 37 | Korean travel accessories       | Mini refill perfume bottle     |
| 38 | Korean travel accessories       | Luggage shoe bag               |
| 39 | Korean pet accessories          | Pet grooming glove             |
| 40 | Korean pet accessories          | Portable pet water bottle      |
| 41 | Korean pet accessories          | Pet food storage container     |
| 42 | Korean pet accessories          | Silicone pet bath brush        |
| 43 | Korean pet accessories          | Pet hair remover roller        |


> To extend you list visit this web page [100 product list for dropshipping ](https://www.wix.com/blog/dropshipping-products?utm_source=google&utm_medium=cpc&utm_campaign=21355403034^163422834859^search%20-%20dsa&experiment_id=^^726585089655^&gad_source=1&gad_campaignid=21355403034&gbraid=0AAAAADwEfwUDBriSsyvRd-ny_CZ_pKMAe&gclid=CjwKCAjw5s_QBhAdEiwADD_gBpvl6PnOJy_B8RwB2sViNEH380inOu0vgGTli8b7HTG0K-eBRtWiqhoCM9QQAvD_BwE)