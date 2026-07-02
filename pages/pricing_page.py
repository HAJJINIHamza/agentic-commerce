import sys
from pathlib import Path

#Fixing import problems
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd 

from agents.pricing_optimization.product_pricing import ProductSellingPriceAgent

st.title("Shopee products pricing calculator")

st.subheader("Upload values from file")
if "upload_file_mode" not in st.session_state:
    st.session_state.upload_file_mode = False

if st.button("Upload values from file"):
    st.session_state.upload_file_mode = True

if st.session_state.upload_file_mode:
    with st.form("uploaded_file_form"):

        uploaded_file = st.file_uploader("Upload product details (csv)", type = ["csv"])
        product_id = st.text_input("Enter product id")

        filled_info = st.form_submit_button("Calculate")

        if filled_info:
            product_data = pd.read_csv(uploaded_file, sep=";", encoding_errors="ignore")
            print ("product_data :", product_data)
            product_data["id"] = product_data["id"].astype(str)
            product_id = str(product_id).strip()

            print ("product id is :", product_id)
            print (product_data["id"].values)

            if product_id not in product_data["id"].values:
                st.error("Product id not found in the uploaded data. Please check and try again.")

            else:
                product_pricing_agent = ProductSellingPriceAgent(product_data)
                product_price, product_price_details = product_pricing_agent.get_product_selling_price(product_id)

                st.subheader(f"Required selling price")
                st.metric(f"The selling price for product {product_id} is: ", f"{product_price} $" )
                st.metric(f"Fixed cost for product {product_id} is: ", f"{product_price_details['fixed_cost']} $")
                st.metric(f"Total rate for product {product_id} is: ", f"{product_price_details['total_rate'] * 100:.2f} %" )

                st.subheader(f"Profit and margin simulation")
                simulated_selling_price = st.number_input("Enter a selling price to simulate profit and margin")

                if simulated_selling_price:
                    profit, margin = product_pricing_agent.simulate_profit(product_id, float(simulated_selling_price))
                    st.metric(f"For selling price {simulated_selling_price} profit is: ", f"{profit} $")
                    st.metric(f"For selling price {simulated_selling_price} margin is: ", f"{margin * 100:.2f} %" )
                
                st.subheader(f"Selling price simulation for target margin")
                target_margin = st.number_input("Enter a target margin to simulate required selling price")
                if target_margin:
                    if target_margin > 1 or target_margin < 0:
                        st.error("Invalid value for target margin, please enter a value between 0 and 1")

                    else:
                        required_selling_price = product_pricing_agent.simulate_selling_price_given_margin(product_id, target_margin)
                        st.metric(f"For target margin {target_margin * 100:.2f} % required selling price is: ", f"{required_selling_price} $")

st.subheader("OR")
st.subheader("Enter values manualy")

if "manual_mode" not in st.session_state:
    st.session_state.manual_mode = False

if st.button("Enter values manually"):
    st.session_state.manual_mode = True

if st.session_state.manual_mode :
    with st.form("manual_values_form"):
        #Fixed cost
        product_cost = st.number_input ("Product cost")
        shipping_cost = st.number_input ("Shipping costs")
        packaging_cost = st.number_input ("Packaging costs")
        international_shipping_cost = st.number_input ("International shipping costs")
        platform_fees = st.number_input ("Platform fees")
        advertising_cost = st.number_input("Advertising_cost")
        payment_fees = st.number_input ("Payment fees")
        #Total rate
        commission_rate = st.number_input("Commission rate")
        transaction_fee_rate = st.number_input("Transaction fee rate")
        payoneer_fee_rate = st.number_input("Payoneer fee rate")
        service_fee_rate = st.number_input("Service fee rate")
        ad_cost_rate = st.number_input ("Ad cost rate")
        target_margin_rate = st.number_input("Target margin rate")

        submit_manual = st.form_submit_button("Calculate")

        if submit_manual:
            product_id = "000"
            df = {  "id" : [product_id],
                    "product_cost" : [product_cost] ,
                    "shipping_cost" : [shipping_cost],
                    "packaging_cost" : [packaging_cost],
                    "international_shipping_cost" : [international_shipping_cost],
                    "platform_fees" : [platform_fees],
                    "advertising_cost" : [advertising_cost],
                    "payment_fees" : [payment_fees],
                    "commission_rate" : [commission_rate],
                    "transaction_fee_rate" : [transaction_fee_rate],
                    "payoneer_fee_rate" : [payoneer_fee_rate],
                    "service_fee_rate" : [service_fee_rate],
                    "ad_cost_rate" : [ad_cost_rate],
                    "target_margin_rate" : [target_margin_rate]}
                
            product_data = pd.DataFrame(df)
            product_pricing_agent = ProductSellingPriceAgent(product_data)
            product_price, product_price_details = product_pricing_agent.get_product_selling_price(product_id)

            st.subheader(f"Required selling price")
            st.metric(f"The selling price for product {product_id} is: ", f"{product_price} $" )
            st.metric(f"Fixed cost for product {product_id} is: ", f"{product_price_details['fixed_cost']} $")
            st.metric(f"Total rate for product {product_id} is: ", f"{product_price_details['total_rate'] * 100:.2f} %" )

            st.subheader(f"Profit and margin simulation")
            simulated_selling_price = st.number_input("Enter a selling price to simulate profit and margin")

            if simulated_selling_price:
                profit, margin = product_pricing_agent.simulate_profit(product_id, float(simulated_selling_price))
                st.metric(f"For selling price {simulated_selling_price} profit is: ", f"{profit} $")
                st.metric(f"For selling price {simulated_selling_price} margin is: ", f"{margin * 100:.2f} %" )
            
            st.subheader(f"Selling price simulation for target margin")
            target_margin = st.number_input("Enter a target margin to simulate required selling price")
            if target_margin:
                if target_margin > 1 or target_margin < 0:
                    st.error("Invalid value for target margin, please enter a value between 0 and 1")

                else:
                    required_selling_price = product_pricing_agent.simulate_selling_price_given_margin(product_id, target_margin)
                    st.metric(f"For target margin {target_margin * 100:.2f} % required selling price is: ", f"{required_selling_price} $")



#To test use command
# streamlit run pages/pricing_page.py
