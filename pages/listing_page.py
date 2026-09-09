import html
import re
import sys
from pathlib import Path

#Fixing import problems
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
import pandas as pd
import streamlit as st 
from src.utils import save_csv_file
from agents.listing_generation.listing_generator import listingGenerationAgent
from agents.listing_generation.listing_evaluator import listingEvaluatorAgent
from src.ui.listings_ui import title_card, title_card_v2, recommended_title_card, description_card, recommended_listing_card

st.title("Product Listings Agent")

if "manual_mode" not in st.session_state:
    st.session_state.manual_mode = False

if st.button("Enter product information"):
    st.session_state.manual_mode = True

if st.session_state.manual_mode:
    with st.form("product_information_form"):
        product_id = st.text_input("Product id")
        product_name = st.text_input("Product name")
        product_category = st.text_input("Product category")
        product_details = st.text_input("Product details")

        submit_form = st.form_submit_button("Generate")

        if submit_form:
            if not all([
                product_id.strip(),
                product_name.strip(),
                product_category.strip(),
                product_details.strip()
            ]):
                st.error("The following fields are required : Product id, Product name, Product catefory and product details.")

            else :
                #Generate Title 
                with st.empty():
                    st.info("⏳ Generating listings, please wait...")
                    title, list_of_titles = listingGenerationAgent().generate_product_title(product_id,
                                                                                            product_name,
                                                                                            product_category,
                                                                                            product_details)
                                                                                    
                    st.empty()

                st.subheader("Product listings")

                st.write(f"**Extracted titles from SHOPEE competitors** :" )
                position = 1
                for extracted_title in list_of_titles:
                    extracted_title = html.escape(extracted_title)
                    if position % 3 == 1:
                        cols = st.columns(3)
                        with cols[0]:
                            title_card(extracted_title)
                    elif position % 3 == 2:
                        with cols[1]:
                            title_card(extracted_title)
                    else:
                        with cols[2]:
                            title_card(extracted_title)
                    position += 1
                st.write(" ")
    
                #st.write(f"**Recommended Title** :")
                recommended_title = title["title"]

                # Clean possible HTML accidentally returned by the LLM
                recommended_title = re.sub(r"<[^>]+>", "", recommended_title)
                recommended_title = html.unescape(recommended_title)
                recommended_title_card(recommended_title)


                #Generate Description
                with st.empty():
                    st.info("⏳ Generating product description, please wait...")
                    product_description, list_of_descriptions = listingGenerationAgent().generate_product_description(product_id,
                                                                                                                    product_name,
                                                                                                                    product_category,
                                                                                                                    product_details)
                    st.empty()

                st.write(f"**Extracted descriptions from SHOPEE competitors** :" )
                for extracted_description in list_of_descriptions:
                    description_card(extracted_description)
                    st.write(" ")

                st.write(f"**Recommended Description** :")
                recommended_description = product_description['description']
                recommended_description = re.sub(r"<[^>]+>", "", recommended_description)
                recommended_description = html.unescape(recommended_description)
                recommended_listing_card(recommended_description, "Recommended Description")
                st.write(" ")

                st.write(f"**Recommended Keywords** :")
                recommended_listing_card(', '.join(product_description['key_words']), "Recommended Keywords")

                
                #try :
                #    with st.empty():
                #        st.info("⏳ Evaluating listings, please wait...")
                #        eval_results = listingEvaluatorAgent().evaluate_listings(product_name,
                #                                                                product_category,
                #                                                                forbidden_claims,
                #                                                                listings["title"],
                #                                                                listings["keywords"],
               #                                                                 listings["description"],
               #                                                                 listings["safe_claims"],
                #                                                                tiktok_listings["tiktok_hook"],
                #                                                                tiktok_listings["tiktok_short_video_script"])
                #        st.empty()
                #except Exception as e:
                #    st.error(f"Couldn't use AI judge to evaluate listings. Error : {e}")

                #Evaluate listings
                #if eval_results["accepted"] == True:
                #    st.success("Listings are safe to be pusblished")
                
                #elif eval_results["accepted"] == False:
                #    st.error("Listings have been rejected by AI juge")
                #    st.info(f"Reason : {eval_results["reason"]}")

                listings_dataframe = pd.DataFrame([
                        {
                            "title": title.get("title"),
                            "description": json.dumps(product_description.get("description")),
                            "safe_claims": json.dumps(product_description.get("safe_claims")),
                            #"accepted": eval_results.get("accepted"),
                            #"reason": eval_results.get("reason")
                        }
                    ])
                
                save_csv_file(listings_dataframe, "listings", "data/listings")
                st.write ("Saved data")