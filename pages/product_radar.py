import sys
from pathlib import Path

#Fixing import problems
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px 
from agents.products_scoring.product_scoring import ProductScoringAgent

st.set_page_config(page_title="LLM Core AI (Inc) Agentic Commerce") 

st.title("Product Radar")
 
uploaded_file = st.file_uploader("Upload products (csv)", type=["csv"]) 
 
if uploaded_file: 
    print("Reading file...")
    product_data = pd.read_csv(uploaded_file, sep=";", encoding_errors="ignore")

    df = {  "product_id": [],
            "product_name": [],
            "product_category": [],
            "product_score": [],
            "demand_growth": [],
            "low_competition_score": [],
            "expected_margin": [],
            "logistics_simplicity": [],
            "supplier_reliability": [],
            "tiktok_virality": [],
            "compliance_safety": [],
            "classification": [],
            "classification_reason": []
        }

    for product_id in product_data["id"].values:
        product_scoring_agent = ProductScoringAgent(product_data)
        product_score, score_components = product_scoring_agent.score_product(product_id)
        df["product_id"].append(product_id)
        df["product_name"].append(product_data.loc[product_data["id"] == product_id, 
                                                   "product_name"].iloc[0])
        df["product_category"].append(product_data.loc[product_data["id"] == product_id, 
                                                       "product_category"].iloc[0].strip())
        df["product_score"].append(product_score)
        df["demand_growth"].append(score_components["demand_growth"])
        df["low_competition_score"].append(score_components["low_competition_score"])
        df["expected_margin"].append(score_components["expected_margin"])
        df["logistics_simplicity"].append(score_components["logistics_simplicity"])
        df["supplier_reliability"].append(score_components["supplier_reliability"])
        df["tiktok_virality"].append(score_components["tiktok_virality"])
        df["compliance_safety"].append(score_components["compliance_safety"])
        df["classification"].append(score_components["classification"])
        df["classification_reason"].append(score_components["classification_reason"])

    df = pd.DataFrame(df)
    df.sort_values(by="product_score", ascending=False, inplace=True)

    st.dataframe(df) 
 
    top_product = df.iloc[0] 
    score_component_names = ["demand_growth", 
                            "low_competition_score", 
                            "expected_margin", 
                            "logistics_simplicity", 
                            "supplier_reliability", 
                            "tiktok_virality", 
                            "compliance_safety"]
    
    #fig, ax = plt.subplots(figsize=(10, 6))
    #sns.barplot(x=score_component_names, y=top_product[score_component_names].values, ax=ax)
    #ax.tick_params(axis="x", rotation=-45)
    #ax.set_ylim(0, 1)

    plotly_df = pd.DataFrame({
        "component_name": score_component_names,
        "component_score": top_product[score_component_names].values
    })
    fig = px.bar(
    plotly_df,
    x="component_name",
    y="component_score",
    title="Score details"
    )

    fig.update_layout(
        xaxis_tickangle=45
    )

    fig.update_yaxes(
        range=[0, 1]
    )

    st.subheader("Top Recommendation") 
    st.write(f"**Name** : **{top_product['product_name']}**") 
    st.write(f"**Category** : **{top_product['product_category']}**")
    st.metric("**Score** :", f"{top_product['product_score']:.2f}") 
    ##st.pyplot(fig)
    st.plotly_chart(fig, use_container_width=True)
 
    if top_product["classification"] == "Great product": 
        st.success("Great product, strong candidate for Shopee testing.") 

    elif top_product["classification"] == "Test": 
        st.info("Good product, Possible candidate for small scale testing .")  
    
    elif top_product["classification"] == "Investigate":
        st.warning ("Score is medium. Investigate product further.")

    elif top_product["classification"] == "Reject": 
        st.error(f"Bad product. Reject immediately, reason : {top_product['classification_reason']}.") 


#USE THIS COMMAND TO LAUNCH THE APP : streamlit run pages/product_radar.py