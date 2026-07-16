import os 
import json
import requests
from dotenv import load_dotenv

from agents.listing_generation.listing_generator import listingGenerationAgent
from src.logger import get_logger

logger = get_logger(__name__)
#
load_dotenv()
os.getenv("OPENROUTER_API_KEY")

class listingEvaluatorAgent():
    def __init__(self):
        pass
    
    def build_evaluation_prompt(self, 
                                product_name, 
                                product_category,
                                forbidden_claims,
                                title,
                                keywords,
                                description,
                                safe_claims,
                                tiktok_hook,
                                tiktok_short_video_script):
        
        with open("agents/prompts/evaluation_prompt.txt", "r") as file:
            evaluation_prompt = file.read()

        return evaluation_prompt.format(product_name = product_name, 
                                        product_category = product_category,
                                        forbidden_claims = forbidden_claims,
                                        title = title,
                                        keywords = keywords,
                                        description = description,
                                        safe_claims = safe_claims,
                                        tiktok_hook = tiktok_hook,
                                        tiktok_short_video_script = tiktok_short_video_script) 

    def evaluate_listings(self,
                          product_name, 
                            product_category,
                            forbidden_claims,
                            title,
                            keywords,
                            description,
                            safe_claims,
                            tiktok_hook,
                            tiktok_short_video_script):
        logger.info("Evaluating generated listings...")
        evaluation_prompt = self.build_evaluation_prompt(product_name, 
                                                        product_category,
                                                        forbidden_claims,
                                                        title,
                                                        keywords,
                                                        description,
                                                        safe_claims,
                                                        tiktok_hook,
                                                        tiktok_short_video_script)
        
        evaluation_results, _ = listingGenerationAgent().get_completion_from_model(evaluation_prompt)

        try : 
            evaluation_results = evaluation_results.replace("```json", "").replace("```", "").strip()
            evaluation_results = json.loads(evaluation_results)
        
        except Exception as e: 
            logger.info("Failed to get a valid evaluation response from model")
            raise ValueError(f"Failed to get valide evaluation response from model, error : {e}")
        
        logger.info(f"Evaluation results : {evaluation_results}")
        if evaluation_results["accepted"] == True:
            logger.info("Postive : Listings accepted to be published")
        else :
            logger.info("Negative : Listings were rejected by model")

        return evaluation_results

    



