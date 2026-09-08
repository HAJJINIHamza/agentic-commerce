import json 
import requests
import time
import random
import os 
from dotenv import load_dotenv
from data_pipeline.collectors.shopee_listings_scrapper import get_product_titles_from_page, get_product_description_from_all_pages

from src.logger import get_logger

logger = get_logger(__name__)

#env
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

class listingGenerationAgent:
    def __init__(self):
        pass

    def get_completion_from_model(
        self,
        prompt: str,
        #"google/gemma-4-31b-it:free" 
        # "meta-llama/llama-3.3-70b-instruct:free" 
        # "meta-llama/llama-3.2-3b-instruct:free" 
        # "openai/gpt-oss-20b:free"
        model_id: str = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        max_retries: int = 5
    ):
        """
        Get a completion from the specified model using the OpenRouter API.
        
        Returns:
            content: The generated text from the model.
            reasoning_details: Additional reasoning details provided by the model.
        """

        logger.info(f"Calling model {model_id}")

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model_id,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "reasoning": {
                "enabled": True
            }
        }

        for attempt in range(max_retries + 1):

            try:

                response = requests.post(
                    url=url,
                    headers=headers,
                    json=payload,
                    timeout=120
                )

                json_response = response.json()

                # Success
                if response.ok and "error" not in json_response:

                    content = json_response["choices"][0]["message"]["content"]

                    reasoning_details = (
                        json_response["choices"][0]["message"]
                        .get("reasoning_details")
                    )

                    logger.info(
                        f"Got completion from model {model_id}"
                    )

                    return content, reasoning_details

                # Error
                error_message = (
                    json_response
                    .get("error", {})
                    .get("message", str(json_response))
                )

                logger.warning(
                    f"Model request failed "
                    f"(attempt {attempt + 1}/{max_retries + 1}): "
                    f"{error_message}"
                )

                # Last attempt → give up
                if attempt == max_retries:
                    raise Exception(
                        f"Model failed after {max_retries + 1} attempts: "
                        f"{error_message}"
                    )

                # Exponential backoff + jitter
                delay = min(2 ** attempt, 30)
                delay += random.uniform(0, 1)

                logger.info(
                    f"Retrying in {delay:.2f} seconds..."
                )

                time.sleep(delay)

            except requests.exceptions.RequestException as e:

                logger.warning(
                    f"Request exception "
                    f"(attempt {attempt + 1}/{max_retries + 1}): {e}"
                )

                if attempt == max_retries:
                    raise

                delay = min(2 ** attempt, 30)
                delay += random.uniform(0, 1)

                time.sleep(delay)

    def get_predifined_prompts(self):

        with open("agents/prompts/title_generation_prompt.txt", "r") as prompt_file:
            title_generation_prompt = prompt_file.read()

        with open("agents/prompts/description_generation_prompt.txt", "r") as prompt_file:
            description_generation_prompt = prompt_file.read()

        #with open("agents/prompts/listing_generation_prompt.txt", "r") as prompt_file:
            #listing_generation_prompt = prompt_file.read()

        #with open("agents/prompts/tiktok_listing_prompt.txt", "r") as prompt_file:
            #tiktok_listing_prompt = prompt_file.read()

        #return ,listing_generation_prompt, tiktok_listing_prompt
        return {"title_generation_prompt": title_generation_prompt, 
                "description_generation_prompt": description_generation_prompt}

    def build_listing_generation_prompt(self,
                                        prompt: str,
                                        target_country: str,
                                        product_name: str,
                                        product_category: str,
                                        main_benefit: str,
                                        buyer_persona: str,
                                        forbidden_claims: str,
                                        ):
        return prompt.format(
            target_country = target_country,
            product_name = product_name,
            product_category = product_category,
            main_benefit = main_benefit,
            buyer_persona = buyer_persona,
            forbidden_claims = forbidden_claims
        )

    def build_title_generation_prompt(self, 
                                      prompt: str,
                                      product_name: str,
                                      product_category: str,
                                      product_details: str,
                                      list_of_titles: list[str]):

        return prompt.format(
            product_name = product_name,
            product_category = product_category,
            product_details = product_details,
            list_of_titles = list_of_titles,
        )

    def build_description_generation_prompt(self,
                                            prompt: str,
                                            product_name: str,
                                            product_category: str,
                                            product_details: str,
                                            list_of_descriptions: list[str]):
        return prompt.format(
            product_name = product_name,
            product_category = product_category,
            product_details = product_details,
            list_of_descriptions = list_of_descriptions,
        )

    #############################################################################################################################
    # VERSION 1 
    #############################################################################################################################
    
    def generate_listings(self, 
                          target_country: str,
                          product_name: str,
                          product_category: str,
                          main_benefit: str,
                          buyer_persona: str,
                          forbidden_claims: str
                          ) : 
        """
        Generate listings based on product details
        """
        #Generate listings 
        logger.info("Generating listings...")
        listing_prompt, tiktok_prompt = self.get_predifined_prompts()
        
        listing_prompt = self.build_listing_generation_prompt(listing_prompt,
                                                                target_country,
                                                                product_name,
                                                                product_category,
                                                                main_benefit,
                                                                buyer_persona,
                                                                forbidden_claims)
        tiktok_prompt = self.build_listing_generation_prompt(tiktok_prompt,
                                                                target_country,
                                                                product_name,
                                                                product_category,
                                                                main_benefit,
                                                                buyer_persona,
                                                                forbidden_claims)
        
        listings, _ = self.get_completion_from_model(listing_prompt)
        tiktok_listings, _ = self.get_completion_from_model(tiktok_prompt)

        try:
            listings = listings.replace("```json", "").replace("```", "").strip()
            listings = json.loads(listings)
        except:
            logger.info("Failed to get a valid json listing response from model")
            raise ValueError("Couldn't get a valid json listing response from model")

        try:
            tiktok_listings = tiktok_listings.replace("```json", "").replace("```", "").strip()
            tiktok_listings = json.loads(tiktok_listings)  
        except Exception as e:
            logger.info("Failed to get a valid json listing response from model")
            raise ValueError(f"Couldn't get a valid json tiktok listings response from model, error : {e}")
        
        logger.info("Successfully generated listings")
        logger.info(f"listings : {listings}")
        logger.info(f"tiktok_listings : {tiktok_listings}")
        return listings, tiktok_listings

    #############################################################################################################################
    # VERSION 2
    #############################################################################################################################
    
    def generate_product_title(self, 
                               product_id, 
                               product_name, 
                               product_category,
                               product_details):
        """
        Generate product title based on product details and competitor titles
        """
        
        product_titles_dict = get_product_titles_from_page(product_id, product_name)
        #product_titles_dict.pop("id", None)
        list_of_titles = product_titles_dict.get("list_of_titles", [])
        if not list_of_titles:
            logger.info("No competitor titles found, using product name as title")
            list_of_titles = [product_name]

        predifined_prompts = self.get_predifined_prompts()
        title_generation_prompt = predifined_prompts["title_generation_prompt"]
        title_generation_prompt = self.build_title_generation_prompt(title_generation_prompt,
                                                                    product_name,
                                                                    product_category,
                                                                    product_details,
                                                                    list_of_titles)
        logger.info("Got and build title generation prompt")

        title, _ = self.get_completion_from_model(title_generation_prompt)

        try:
            title = title.replace("```json", "").replace("```", "").strip()
            title = json.loads(title)
        except:
            logger.info("Failed to get a valid json title response from model")
            raise ValueError("Couldn't get a valid json title response from model")

        logger.info("Successfully generated title")
        logger.info(f"title : {title}")
        return title

    def generate_product_description(self,
                                     product_id,
                                     product_name,
                                     product_category,
                                     product_details):
        """
        Generate product description based on product details and competitor descriptions
        """

        product_descriptions_dict = get_product_description_from_all_pages(product_id, product_name)
        list_of_descriptions = product_descriptions_dict.get("descriptions", [])
        if not list_of_descriptions:
            logger.info("No competitor descriptions found, using product details as description")
            list_of_descriptions = [product_details]

        #description_generation_prompt
        description_generation_prompt = self.get_predifined_prompts()["description_generation_prompt"]
        description_prompt = self.build_description_generation_prompt(description_generation_prompt,
                                                product_name,
                                                product_category,
                                                product_details,
                                                list_of_descriptions)

        product_description, _ = self.get_completion_from_model(description_prompt)
        try:
            product_description = product_description.replace("```json", "").replace("```", "").strip()
            product_description = json.loads(product_description)
        except:
            logger.info("Failed to get a valid json product_description response from model")
            raise ValueError("Couldn't get a valid json product_description response from model")

        logger.info("Successfully generated product description")
        logger.info(f"product_description : {product_description}")
        return product_description









        







