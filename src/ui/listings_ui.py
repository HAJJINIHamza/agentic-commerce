import streamlit as st
import textwrap

def title_card(title):
    st.markdown(
        f"""
        <div style="
            border: 1px solid #d9d9d9;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            background-color: #fafafa;
            height: 120px;
            overflow: hidden;
            box-sizing: border-box;
        ">
            <p style="
                margin: 0;
                font-size: 15px;
                line-height: 1.5;
            ">
                {title}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def title_card_v2(title):
    st.markdown(
        f"""<div style="
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
            background-color: white;
            min-height: 100px;
            box-sizing: border-box;
        ">
            <div style="
                font-size: 12px;
                color: #888;
                margin-bottom: 8px;
            ">Competitor Title</div><div style="
                font-size: 15px;
                line-height: 1.5;
                color: #222;
            ">{title}</div>
        </div>""",
        unsafe_allow_html=True
    )

def recommended_title_card(recommended_title):
    st.markdown(
        f"""<div style="
            border: 2px solid #4A90E2;
            border-radius: 12px;
            padding: 20px;
            margin-top: 10px;
            margin-bottom: 20px;
            background-color: #F7FBFF;
            box-sizing: border-box;
        ">
            <div style="
                font-size: 13px;
                font-weight: 600;
                color: #4A90E2;
                margin-bottom: 10px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            ">✨ Recommended Title</div><div style="
                font-size: 17px;
                font-weight: 600;
                line-height: 1.5;
                color: #222;
            ">{recommended_title}</div>
        </div>""",
        unsafe_allow_html=True
    )

def description_card(description):
    st.markdown(
        f"""
        <div style="
            border: 1px solid #d9d9d9;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            background-color: #fafafa;
            height: 360px;
            overflow: hidden;
            box-sizing: border-box;
        ">
            <p style="
                margin: 0;
                font-size: 15px;
                line-height: 1.5;
            ">
                {description}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def recommended_description_card(recommended_description):
    st.markdown(
        f"""<div style="
            border: 2px solid #4A90E2;
            border-radius: 12px;
            padding: 20px;
            margin-top: 10px;
            margin-bottom: 20px;
            background-color: #F7FBFF;
            box-sizing: border-box;
        ">
            <div style="
                font-size: 13px;
                font-weight: 600;
                color: #4A90E2;
                margin-bottom: 10px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            ">✨ Recommended Description</div><div style="
                font-size: 17px;
                font-weight: 600;
                line-height: 1.5;
                color: #222;
            ">{recommended_description}</div>
        </div>""",
        unsafe_allow_html=True
    )

def recommended_listing_card(listings, name_of_listing="Recommended Listing"):
    st.markdown(
        f"""<div style="
            border: 2px solid #4A90E2;
            border-radius: 12px;
            padding: 20px;
            margin-top: 10px;
            margin-bottom: 20px;
            background-color: #F7FBFF;
            box-sizing: border-box;
        ">
            <div style="
                font-size: 13px;
                font-weight: 600;
                color: #4A90E2;
                margin-bottom: 10px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            ">✨ {name_of_listing}</div><div style="
                font-size: 17px;
                font-weight: 600;
                line-height: 1.5;
                color: #222;
            ">{listings}</div>
        </div>""",
        unsafe_allow_html=True
    )