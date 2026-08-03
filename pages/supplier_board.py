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
from agents.supplier_scoring.supplier_contacting import ContactSupplier

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
            "product_cost_score": [],
            "moq_score": [],
            "images_quality_score": [],
            "supplier_response_time_score": [],
            "supplier_tenure_score": [],
            "place_of_origin_score": [],
            "classification": []
        }
    
    print ("supplier name :", suppliers_data["supplier_name"])
    for supplier_id in suppliers_data["supplier_id"].values:
        supplier_scoring_agent = supplierScoringAgent(suppliers_data)
        supplier_score, score_components = supplier_scoring_agent.compute_supplier_score(supplier_id)

        df["supplier_id"].append(supplier_id)
        df["product_id"].append(suppliers_data.loc[suppliers_data["supplier_id"] == supplier_id, 
                                                   "product_id"].iloc[0])
        df["supplier_name"].append(suppliers_data.loc[suppliers_data["supplier_id"] == supplier_id, 
                                                   "supplier_name"].iloc[0])
        df["product_name"].append(suppliers_data.loc[suppliers_data["supplier_id"] == supplier_id, 
                                                   "product_name"].iloc[0])
        df["supplier_score"].append(supplier_score)
        df["product_cost_score"].append(score_components["supplier_product_cost_score"])
        df["moq_score"].append(score_components["moq_score"])
        df["images_quality_score"].append(score_components["images_quality_score"])
        df["supplier_response_time_score"].append(score_components["supplier_response_time_score"])
        df["supplier_tenure_score"].append(score_components["supplier_tenure_score"])
        df["place_of_origin_score"].append(score_components["place_of_origin_score"])
        df["classification"].append(score_components["classification"])

    df = pd.DataFrame(df)
    df.sort_values(by="supplier_score", ascending=False, inplace=True)
    save_csv_file(df, "supplier_scores", "data/supplier_scorings/supplier_scores/")

    st.dataframe(df) 
 
    top_supplier = df.iloc[0] 
    score_component_names = [
                            "product_cost_score", 
                            "moq_score", 
                            "images_quality_score",
                            "supplier_response_time_score", 
                            "supplier_tenure_score",
                            "place_of_origin_score",    
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

    st.write("TOP supplier information")
    top_supplier_data = suppliers_data[suppliers_data["supplier_id"] == top_supplier["supplier_id"]]
    st.dataframe(top_supplier_data)


    if top_supplier["classification"] == "Excelent":
        st.success("Excelent supplier, strong candidate for testing")
    
    elif top_supplier["classification"] == "Qualified":
        st.success("Qualified supplier, good for testing")
    
    elif top_supplier["classification"] == "Review" :
        st.warning("Meduim supplier, need further investigation")
    
    else : 
        st.error("Bad supplier, to avoid")
    
    st.subheader("Email to send to supplier")
    top_supplier_id = top_supplier["supplier_id"]
    product_name = suppliers_data.loc[suppliers_data["supplier_id"] == supplier_id, "product_name"].values[0]
    product_cost = suppliers_data.loc[suppliers_data["supplier_id"] == supplier_id, "product_cost"].values[0]
    moq = suppliers_data.loc[suppliers_data["supplier_id"] == supplier_id, "moq"].values[0]
    email = ContactSupplier().get_contacting_mail(product_name, 
                                                  product_cost,
                                                  moq)
    st.write(email)
    

#USE THIS COMMAND TO LAUNCH THE APP : streamlit run pages/product_radar.py