import json 
import requests
import os 
from dotenv import load_dotenv

from src.logger import get_logger

logger = get_logger(__name__)

#env
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

class listingGenerationAgent:
    def __init__(self):
        pass

    def get_completion_from_model(self,
                                  prompt : str, 
                                  model_id : str = "google/gemma-4-31b-it:free"):
        """
        Get completion of a prompt from a model

        Returns:

        - Content
        - Reasoning details
        """
        response = requests.post(
                        url = "https://openrouter.ai/api/v1/chat/completions",
                        headers= {
                            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                            "Content-Type": "application/json",
                            #"HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
                            #"X-OpenRouter-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
                        },
                        data=json.dumps({
                        "model": model_id,
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                            ],
                        "reasoning": {"enabled": True}
                        })
                        )
        
        json_response = response.json()
        if "error" in response:
            logger.info(f"[WARNING] failed to get completion from model, because {response["error"]["message"]}")
            raise Exception(response["error"]["message"])
        content = json_response["choices"][0]["message"]["content"]
        reasoning_details = json_response["choices"][0]["message"]["reasoning_details"]
        logger.info("Got completion from model")
        return content, reasoning_details

    def get_predifined_prompts(self):

        with open("agents/prompts/listing_generation_prompt.txt", "r") as prompt_file:
            listing_generation_prompt = prompt_file.read()

        with open("agents/prompts/tiktok_listing_prompt.txt", "r") as prompt_file:
            tiktok_listing_prompt = prompt_file.read()
        
        return listing_generation_prompt, tiktok_listing_prompt

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
        except:
            logger.info("Failed to get a valid json listing response from model")
            raise ValueError("Couldn't get a valid json tiktok listings response from model")
        
        logger.info("Successfully generated listings")
        logger.info(f"listings : {listings}")
        logger.info(f"tiktok_listings : {tiktok_listings}")
        return listings, tiktok_listings
    

        


        







