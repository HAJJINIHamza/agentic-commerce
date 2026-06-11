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

### Score supplier 
```
supplier_score(supplier): 
    initiate score = 0 
 
    # Lower MOQ is better 
 
    if supplier["moq"] <= 100: 
        score += 25 
    elif supplier["moq"] <= 300: 
        score += 15 
    else: 
        score += 5 
 
    # Shorter lead time is better 
    if supplier["lead_time_days"] <= 5: 
        score += 25 
    elif supplier["lead_time_days"] <= 10: 
        score += 15 
    else: 
        score += 5 
 
    # Legal and export readiness 
    if supplier["brand_authorization"]: 
        score += 20 
 
    if supplier["export_ready"]: 
        score += 15 
 
    # Communication and quality  
    score += supplier["response_speed_score"] * 10 
    score += supplier["quality_score"] * 5 
 
    return round(score, 2) 
```

> The method used to score supplier in product scoring is:
```
SupplierReliabilityScore = 0.3 * SupplierRatingScore +
                            0.3 * MoqScore +
                            0.2 * ResponseRateScore +
                            0.2 * OrderVolumeScore 
````


### Supplier page 
Type : Dashboard 

Niche : One product

Input : information of the suppliers of one product 

Output : Supplier scorings and top recommandation

