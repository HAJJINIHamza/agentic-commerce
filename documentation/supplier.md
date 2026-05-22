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