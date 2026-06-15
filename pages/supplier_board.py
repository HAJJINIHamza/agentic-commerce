import sys
from pathlib import Path

#Fixing import problems
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils import save_csv_file
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px 
from agents.supplier_scoring.supplier_scoring import supplierScoringAgent

st.set_page_config(page_title="LLM Core AI (Inc) Agentic Commerce") 

st.title("Suppliers dashboard")
 
uploaded_file = st.file_uploader("Upload suppliers (csv)", type=["csv"]) 
 
if uploaded_file: 
    print("Reading file...")
    suppliers_data = pd.read_csv(uploaded_file, sep=";", encoding_errors="ignore")

    df = {  "supplier_id" : [],
            "product_id": [],
            "supplier_name": [],
            "product_name": [],
            "supplier_score" : [],
            "supplier_rating_score": [],
            "moq_score": [],
            "supplier_response_rate_score": [],
            "order_volume_score": [],
            "classification": []
        }

    for supplier_id in suppliers_data["supplier_id"].values:
        supplier_scoring_agent = supplierScoringAgent(suppliers_data)
        supplier_score, score_components = supplier_scoring_agent.compute_supplier_score(supplier_id)

        df["supplier_id"].append(supplier_id)
        df["product_id"].append(suppliers_data.loc[suppliers_data["supplier_id"] == supplier_id, 
                                                   "product_id"].iloc[0])
        print ("supplier names :", suppliers_data["supplier_name"])
        df["supplier_name"].append(suppliers_data.loc[suppliers_data["supplier_id"] == supplier_id, 
                                                   "supplier_name"].iloc[0])
        df["product_name"].append(suppliers_data.loc[suppliers_data["supplier_id"] == supplier_id, 
                                                   "product_name"].iloc[0])
        df["supplier_score"].append(supplier_score)
        df["supplier_rating_score"].append(score_components["supplier_rating_score"])
        df["moq_score"].append(score_components["moq_score"])
        df["supplier_response_rate_score"].append(score_components["supplier_response_rate_score"])
        df["order_volume_score"].append(score_components["order_volume_score"])
        df["classification"].append(score_components["classification"])

    df = pd.DataFrame(df)
    df.sort_values(by="supplier_score", ascending=False, inplace=True)
    save_csv_file(df, "supplier_scores", "data/supplier_scorings/")

    st.dataframe(df) 
 
    top_supplier = df.iloc[0] 
    score_component_names = [
                            "supplier_rating_score", 
                            "moq_score", 
                            "supplier_response_rate_score", 
                            "order_volume_score",
                            "classification" 
                            ]
    
    #fig, ax = plt.subplots(figsize=(10, 6))
    #sns.barplot(x=score_component_names, y=top_product[score_component_names].values, ax=ax)
    #ax.tick_params(axis="x", rotation=-45)
    #ax.set_ylim(0, 1)

    plotly_df = pd.DataFrame({
        "component_name": score_component_names,
        "component_score": top_supplier[score_component_names].values
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
    st.write(f"**Supplier Name** : **{top_supplier['supplier_name']}**") 
    st.write(f"**Supplier id** : **{top_supplier['supplier_id']}**")
    st.metric("**Score** :", f"{top_supplier['supplier_score']:.2f}") 
    ##st.pyplot(fig)
    st.plotly_chart(fig, use_container_width=True)


    if top_supplier["classification"] == "Excelent":
        st.success("Excelent supplier, strong candidate for testing")
    
    elif top_supplier["classification"] == "Qualified":
        st.success("Qualified supplier, good for testing")
    
    elif top_supplier["classification"] == "Review" :
        st.warning("Meduim supplier, need further investigation")
    
    else : 
        st.error("Bad supplier, to avoid")
    

#USE THIS COMMAND TO LAUNCH THE APP : streamlit run pages/product_radar.py