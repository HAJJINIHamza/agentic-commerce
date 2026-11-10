# Agentic Commerce

Traditional sellers choose products, suppliers, and prices using their intuition and prior experience. They don't collect data about the performance of their sales, so they can't evaluate or improve their choices and decisions.

We propose agentic commerce, an approach that relies on data, business rules, and agentic AI to select winning products and reliable suppliers, estimate competitive prices, and monitor commerce performance to improve decision-making.

|E-commerce platform| Markets | Type of products | Suppliers | Logistics |
| --- | --- | --- | --- | --- |
| <img src="https://cdn.simpleicons.org/shopee/EE4D2D" alt="Shopee logo" width="28"> SHOPEE | 🇸🇬 Singapore (main) - 🇹🇼 Taiwan - 🇹🇭 Thailand - 🇲🇾 Malaysia - 🇻🇳 Vietnam | K-beauty products | 🇰🇷 Korean suppliers, <img src="https://cdn.simpleicons.org/alibabadotcom/FF6A00" alt="Alibaba.com logo" width="28"> Alibaba, etc. | 🚚 EXPRESS Couriers - <img src="https://ep-website-media.s3.ap-southeast-1.amazonaws.com/sg/wp-content/uploads/2025/06/spx-express-logo.png" alt="SPX Express logo" width="72"> Shopee logistics service|

### Toolbox
<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas">
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" alt="PyTorch">
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white" alt="LangChain">
  <img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square&logo=langgraph&logoColor=white" alt="LangGraph">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white" alt="Git">
</p>

|tool | version |
| --- | --- |
| python | 3.12.3 |
| pandas | 3.0.3 |
| streamlit | 1.58.0 |
| torch | 2.11.0 |
| langchain | 1.0.3 |

### Project components
1. Product discovery and selection

    It starts by preparing a large list of the best-selling products on Shopee in the specified markets. Then, it ranks the products using collected data and mathematical formulas. Finally, it recommends the top 10 products to be listed on Shopee. These products are the most likely to provide a return on investment.

    The product rankings are based on product costs, market prices, estimated profit, market demand, competition, social media popularity, ease of logistics, product compliance and regulations, size, and weight.

    ![Product selection](documentation/diagrams/product_selection.drawio.png)

2. Supplier selection

    From a list of suppliers, the agent ranks and selects the most reliable suppliers using their data and mathematical formulas.

    The selection criteria are supplier product costs, location, certifications, MOQ (minimum order quantity), response rate, average number of sales, lead time, and product catalog.

    ![Supplier selection](documentation/diagrams/supplier_selection.drawio.png)

3. Listing generation AI Agent

    Listing our products on Shopee requires an engaging image, title, specifications, description, keywords, and a Q&A section. To generate [optimized listings](#listing-dashboard) that stand out from the competition, I use specialized e-commerce listing agents.
    
    The process starts by analyzing our competitors' listings and extracting relevant patterns and insights about how listings should look and what engages customers. It then generates personalized listings for every product.

    ![Listing generation agent](documentation/diagrams/listing_generation_ai_agent.drawio.png)

4. Product pricing 
    
    The objective is to estimate competitive prices for our products on Shopee. The process starts by extracting our competitors' prices and determining a competitive price range. It then uses a mathematical formula that includes the necessary costs, rates, fees, commissions, and profits to estimate the final price.

    ![Product pricing](documentation/diagrams/product_pricing.drawio.png)

4. Marketing dashboard

    It extracts marketing data from the Shopee platform and generates a dashboard that summarizes the [marketing results](#marketing-agent---marketing-dashboard).

    ![Marketing dashboard](documentation/diagrams/marketing_dashboard.drawio.png)
    
6. Marketing analytics AI Agent

    This is a multi-stage RAG system. Its objective is to use an AI marketing expert to analyze our marketing data, [generate a report](#marketing-analytics-agent---marketing-report-and-decision-making), and then propose practical recommendations to improve our marketing results.

    ![Marketing agent](documentation/diagrams/marketing_analytics_ai_agent.drawio.png)

### Project structure

```text
agentic-commerce/
├── agents/                   # Product, supplier, pricing, listing, and marketing agents
│   ├── embeddings/           # Embedding integrations
│   ├── listing_generation/   # Listing generation, evaluation, and guardrails
│   ├── marketing_analytics/  # Marketing analysis and RAG retrieval
│   │   └── knowledge_base_builders/
│   ├── pricing_optimization/
│   ├── products_scoring/
│   ├── prompts/              # LLM prompts
│   └── supplier_scoring/
├── data/                     # Input data and generated agent outputs
├── data_pipeline/            # Product collection and scraping
│   ├── collectors/
│   └── config/
├── documentation/            # Project notes, guides, and screenshots
├── notebooks/                # Exploratory and test notebooks
├── pages/                    # Streamlit pages for the dashboards
├── ressources/               # Images and RAG reference documents
├── src/                      # Shared utilities and UI components
├── tests/                    # Agent and component tests
├── app.py                    # Streamlit application entry point
├── config.yaml               # Application configuration
├── requirements.txt          # Python dependencies
└── Pipfile                   # Pipenv dependency configuration
```


### Project screens

#### Product selection agent - Product scoring dashboard
![Recommended product](documentation/project_screenshots/recommended_product.png)

### Supplier selection agent - Supplier scoring dashboard
![Recommended supplier](documentation/project_screenshots/recommended_supplier.png)

#### Dynamic pricing agent - Pricing dashboard

![pricing 1](documentation/project_screenshots/pricing_1.png)
![pricing 2](documentation/project_screenshots/pricing_2.png)
![pricing 3](documentation/project_screenshots/pricing_3.png)

#### Marketing Agent - Marketing dashboard

![marketing dashboard](documentation/project_screenshots/marketing_dashboard_screen_1_20-18-2026.png)
![marketing dashboard](documentation/project_screenshots/marketing_dashboard_screen_2_20-18-2026.png)
![marketing dashboard](documentation/project_screenshots/marketing_dashboard_screen_3_20-18-2026.png)

#### Listing Dashboard
![listing dashboard](documentation/project_screenshots/listing_dashboard_1.png)

![listing dashboard](documentation/project_screenshots/listing_dashboard_2.png)

![listing dashboard](documentation/project_screenshots/listing_dashboard_3.png)

![listing dashboard](documentation/project_screenshots/listing_dashboard_4.png)

![listing dashboard](documentation/project_screenshots/listing_dashboard_5.png)

#### Marketing Analytics Agent - Marketing report and decision making
![marketing agent](documentation/project_screenshots/marketing_analyst_agent_screen_1.png)

![marketing agent](documentation/project_screenshots/marketing_analyst_agent_screen_2.png)
