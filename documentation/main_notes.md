### Commerce life cycle : 
1. Find products 
2. Score products, pick top 5
3. Find a supplier for every product
4. Determine the selling price for every product
5. Create a listing (marketing) for every product
6. Lunch sales and monitor performance

### Product : 
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

`Data sources : Shopee API, Shopify API`

Example products: scalp massage brush, silicone facial cleansing pad, makeup puff, cosmetic spatula, cosmetic organizer, travel cosmetic bottle, shower scalp brush, hair towel, compact comb, brush holder. desk organizer, cute stationery, travel pouch, kitchen small tool, 
storage case. 

**Product table**
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

### Suppliers
- Reliable Korean supplier
- MOQ (Minimum Order Quantity) Low -> test with small sample
- Supplier is fast (lead time days)-> Restock quicly 
- Product quality is stable        -> Product consistency
- Can provide documents and images -> Market and sell internationally
- Brand authorization is clear     -> Legally allowed to sell 
- Respond quickly                  -> Quick communication

**Supplier table**
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
)

