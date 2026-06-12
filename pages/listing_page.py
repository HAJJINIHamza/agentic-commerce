import sys
from pathlib import Path

#Fixing import problems
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st 
from agents.listing_generation.listing_generator import listingGenerationAgent
from agents.listing_generation.listing_evaluator import listingEvaluatorAgent

st.title("Product Listings Agent")

if "manual_mode" not in st.session_state:
    st.session_state.manual_mode = False

if st.button("Enter product information"):
    st.session_state.manual_mode = True

if st.session_state.manual_mode:
    with st.form("product_information_form"):
        target_country = st.text_input("Target country")
        product_name = st.text_input("Product name")
        product_category = st.text_input("Product category")
        main_benefit = st.text_input("Main benefit")
        buyer_persona = st.text_input("Buyer persona")
        forbidden_claims = st.text_input("Forbidden claims")

        submit_form = st.form_submit_button("Generate")

        if submit_form:
            if not all([
                product_name.strip(),
                product_category.strip(),
                main_benefit.strip()
            ]):
                st.error("The following fields are required : Product name, Product catefory and main benifit.")

            else :
                #Generate listings 
                with st.empty():
                    st.info("⏳ Generating listings, please wait...")
                    listings, tiktok_listings = listingGenerationAgent().generate_listings(target_country,
                                                                                    product_name,
                                                                                    product_category,
                                                                                    main_benefit,
                                                                                    buyer_persona,
                                                                                    forbidden_claims
                                                                                    )
                    st.empty()

                st.subheader("Product listings")
                
                st.write(f"**Title** : {listings["title"]}")
                st.write(f"**Key words** :" )
                for key_word in listings["keywords"]:
                    st.write(f"- {key_word}")
                st.write(f"**Description** :")
                for description in listings["description"]:
                    st.write(f"- {description}")
                st.write(f"**Safe claims** :")
                for safe_claim in listings["safe_claims"]:
                    st.write(f"- {safe_claim}")
                st.write(f"**TikTok hook** : {tiktok_listings["tiktok_hook"]}")
                st.write(f"**TikTok video script** : {tiktok_listings["tiktok_short_video_script"]}")

                with st.empty():
                    st.info("⏳ Evaluating listings, please wait...")
                    eval_results = listingEvaluatorAgent().evaluate_listings(product_name,
                                                                            product_category,
                                                                            forbidden_claims,
                                                                            listings["title"],
                                                                            listings["keywords"],
                                                                            listings["description"],
                                                                            listings["safe_claims"],
                                                                            tiktok_listings["tiktok_hook"],
                                                                            tiktok_listings["tiktok_short_video_script"])
                    st.empty()

                #Evaluate listings
                if eval_results["accepted"] == True:
                    st.success("Listings are safe to be pusblished")
                
                else :
                    st.error("Listings have been rejected by AI juge")
                    st.info(f"Reason : {eval_results["reason"]}")
