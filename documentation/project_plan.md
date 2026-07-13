### Project Plan 
1. Days 1–3: Understand the business and design data tables 
    Deliverables: 
    - Product database schema 
    - Supplier database schema 
    - Pricing formula 
    - Product scoring formula 
    - First target country list (Shopee Korea)
    - First product category list 

2. Product scoring
    - Fill product data manually in a CSV file
    - develop scoring script (input : product data -> output : product score)
    - Order products by score
    - Develop product pricing script (input: product data -> output : product price)

3. Days 4–7: Build Product Radar MVP :

The first MVP is a simple dashboard that ranks products. 

Input: 
 product name, 
 country, 
 estimated demand, 
 competition, 
 cost, 
 margin, 
 logistics difficulty, 
 supplier reliability, 
 TikTok potential. 

Output: 
 top 20 product candidates, 
 reason for ranking, 
 risk warning. 

4. Build Pricing and Supplier Engine 
    Deliverables: 
    - Supplier database 
    - Pricing calculator 
    - Break-even calculator 
    - Margin simulator 
    - Country-specific price comparison 


5. Week 3: Build Listing and Content Generator 
    Deliverables: 
    - Shopee title generator 
    - Product description generator 
    - Keyword generator 
    - TikTok script generator 
    - Compliance filter






10. Develop Data Pipelines
- Set APIs, AliExpress, AliBaba, ...
- Develop data extraction pipeline
- Process, clean or prepare data
- Store data on product and supplier Databases. 

### TODOs

#### TODO 15-06-2026
- Add save data (excel or csv) at the end of product scoring, supplier scoring, product selling, listing generation (Mostly done)
- Add original data structure (supplier_id, product_id) to product, supplier and listing (In progess)
- Generate some data from Chatgpt and use it for testing, like products and suppliers. (DONE)
- An if else condition to verify compliance safety via category isn't the best approach, think about using an LLM for decision

### TODO 02-07-2026
- Product radar top section should show at least 3 products not only one
- Apply pricing to two more products 
- Add products to shopee
- Add data saving to pricing page and listing page
- Fix the listing generation problem, if llm can't get completion then try again in few seconds automatically or think about switching to a different model
- Add an image generation model, to automatically generate images.
