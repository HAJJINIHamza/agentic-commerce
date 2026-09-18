from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

from agents.marketing_analytics.marketing_agent import marketingAgent
from src.logger import get_logger
from src.ui.marketing_metrics import metric_card, metric_section
from datetime import date

logger = get_logger(__name__)

st.set_page_config(page_title="LLM Core AI (Inc) Agentic Commerce")

st.title("Marketing Analytics Dashboard")

file_path = st.text_input("Enter the path to the Shopee Ads CSV file:", key="file_path")

marketing_agent = marketingAgent()

st.markdown(
    """
    <style>

    .metric-card {
        background: white;
        border: 1px solid #e6e6e6;
        border-radius: 12px;
        padding: 20px 22px;
        min-height: 130px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    .metric-title {
        font-size: 14px;
        font-weight: 600;
        color: #666;
        margin-bottom: 10px;
    }

    .metric-value {
        font-size: 30px;
        font-weight: 700;
        color: #111;
        line-height: 1.2;
    }

    .metric-subtitle {
        font-size: 12px;
        color: #888;
        margin-top: 6px;
    }

    .metric-delta {
        font-size: 13px;
        font-weight: 600;
        margin-top: 8px;
    }

    .delta-positive {
        color: #16803c;
    }

    .delta-negative {
        color: #c62828;
    }

    .delta-neutral {
        color: #777;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>

    .metric-section {
        background: #fafafa;
        border: 1px solid #dedede;
        border-radius: 16px;
        padding: 24px;
        margin: 20px 0;
    }

    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #222;
        margin-bottom: 4px;
    }

    .section-description {
        font-size: 13px;
        color: #777;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

if file_path:
    try : 
        file_path = Path(file_path)
    except Exception as e:
        raise ValueError(f"This is not a valid path {file_path} Error: {e}")
    
    shopee_ads_data = marketing_agent.read_shopee_ads_data(file_path)

    processed_overall_data = marketing_agent.process_overall_data(shopee_ads_data)

    #st.write(f"Date Period: {marketing_metrics['date_period']}")
    #st.write(f"Ad Name: {marketing_metrics['ad_name']}")
    st.subheader("Ad Details :")

    st.markdown(f"""
    | start_date | end_date | Ad name|
    |---|---| --- |
    |{processed_overall_data['start_date'].values[0]} | {processed_overall_data['end_date'].values[0]} | {processed_overall_data['Ad Name'].values[0]}|
    """, unsafe_allow_html=True)

    st.subheader("Performance :")

    cols = st.columns(3)

    with cols[0]:
        metric_card(
            "Impressions",
            f"{processed_overall_data['Impression'].values[0]:,}",
            "Times ads were displayed",
        )

    with cols[1]:
        metric_card(
            "Clicks",
            f"{processed_overall_data['Clicks'].values[0]:,}",
            "Ad clicks",
        )

    with cols[2]:
        metric_card(
            "Orders",
            f"{processed_overall_data['Conversions'].values[0]:,}",
            "Orders attributed to ads",
        )



    # ----------------------------------------------------
    #
    st.text("")
    #
    # ----------------------------------------------------

    cols = st.columns(4)

    with cols[0]:
        metric_card(
            "CTR",
            f"{processed_overall_data['ctr_%'].iloc[0]:,.2f}%",
            "Click Through Rate (%)",
        )


    with cols[1]:
        metric_card(
            "Conversion rate %",
            f"{processed_overall_data['conversion_rate_%'].iloc[0]:,.2f}%",
            "Conversion rate (%)",
        )

    with cols[2]:
        metric_card(
            "Impressions needed",
            f"{processed_overall_data['number_of_impressions_needed'].iloc[0]:,.2f}",
            "Impressions needed for 1 click",
        )

    with cols[3]:
        metric_card(
            "Clicks needed",
            f"{processed_overall_data['number_of_clicks_needed'].iloc[0]:,.2f}",
            "Clicks needed for 1 order",
        )

    # ----------------------------------------------------
    #
    st.text("")
    #
    # ----------------------------------------------------

    cols = st.columns(3)

    with cols[0]:
        metric_card (
            "CPC $",
            f"${processed_overall_data['cpc_$'].iloc[0]:,}",
            "Cost Per Click ($)",
        )

    with cols[1]:
        metric_card (
            "Expense $",
            f"${processed_overall_data['Expense'].values[0]:,}",
            "Total Expense $",
        )

    with cols[2]:
        metric_card(
            "ROAS",
            f"{processed_overall_data['roas_$'].values[0]:,.2f}$",
            "Return on Ad Spend ($)",
        )

    # ----------------------------------------------------
    #
    # Visualise day by day data
    #
    # ----------------------------------------------------

    st.subheader("Day by day analytics :")

    start_date = st.date_input(
        "Start date",
        value=date(2026, 8, 5),
        format="DD-MM-YYYY"
    )
    end_date = st.date_input(
        label = "End date",
        value = date(2026, 8, 12),
        format = "DD-MM-YYYY",
    )

    if st.button("Visualize"):

        if end_date < start_date:
            st.error("Invalid date range: End day must be greater than or equal to Start day.")

        else :
            print ("End date :", end_date)
            print ("Start date :", start_date)
            shopee_day_by_day_data = marketing_agent.process_day_by_day_data(start_date, end_date)

            fig_1 = px.line(shopee_day_by_day_data, 
                    x="start_date", 
                    y="Impression", 
                    markers=True, 
                    title="Impression per day", 
                    height=400, 
                    width=1000,
                        )
            
            #fig_1.update_traces(line_color="crimson")
            st.plotly_chart(fig_1, use_container_width = True)

            fig_2 = px.line(shopee_day_by_day_data, 
                    x="start_date", 
                    y="Clicks", 
                    markers=True, 
                    title="Clicks per day", 
                    height=400, 
                    width=1000,
                        )
            fig_2.update_traces(line_color="crimson")
            st.plotly_chart(fig_2, use_container_width = True)

            fig_3 = px.line(shopee_day_by_day_data, 
                    x="start_date", 
                    y="ctr_%", 
                    markers=True, 
                    title="CTR % per day", 
                    height=400, 
                    width=1000,
                        )
            fig_3.update_traces(line_color="green")
            st.plotly_chart(fig_3, use_container_width = True)

            fig_4 = px.line(shopee_day_by_day_data, 
                    x="start_date", 
                    y="Conversions", 
                    markers=True, 
                    title="Conversions per day", 
                    height=400, 
                    width=1000,
                        )
            fig_4.update_traces(line_color="royalblue")
            st.plotly_chart(fig_4, use_container_width = True)

            fig_5 = px.line(shopee_day_by_day_data, 
                    x="start_date", 
                    y="number_of_impressions_needed", 
                    markers=True, 
                    title="Number of impression needed for 1 click per day", 
                    height=400, 
                    width=1000,
                        )
            #fig_5.update_traces(line_color="royalblue")
            st.plotly_chart(fig_5, use_container_width = True)

            fig_6 = px.line(shopee_day_by_day_data, 
                    x="start_date", 
                    y="cpc_$", 
                    markers=True, 
                    title="CPC $ per day", 
                    height=400, 
                    width=1000,
                        )
            fig_6.update_traces(line_color="crimson")
            st.plotly_chart(fig_6, use_container_width = True)

            fig_7 = px.line(shopee_day_by_day_data, 
                    x="start_date", 
                    y="Expense", 
                    markers=True, 
                    title="Expense $ per day", 
                    height=400, 
                    width=1000,
                        )
            fig_7.update_traces(line_color="forestgreen")
            st.plotly_chart(fig_7, use_container_width = True)





