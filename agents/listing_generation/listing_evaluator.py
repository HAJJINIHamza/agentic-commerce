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
                                description):
        
        with open("agents/prompts/evaluation_prompt.txt", "r") as file:
            evaluation_prompt = file.read()

        return evaluation_prompt.format(product_name = product_name, 
                                        product_category = product_category,
                                        forbidden_claims = forbidden_claims,
                                        title = title,
                                        keywords = keywords,
                                        description = description) 

    def evaluate_listings(self,
                          product_name, 
                            product_category,
                            forbidden_claims,
                            title,
                            keywords,
                            description,
                            max_attempts = 5):

        """
        Evaluates listing 

        Returns : 

        {
        "accepted" : Boolean,
        "reason" : string
        }
        """
        logger.info("Evaluating generated listings...")
        evaluation_prompt = self.build_evaluation_prompt(product_name, 
                                                        product_category,
                                                        forbidden_claims,
                                                        title,
                                                        keywords,
                                                        description)
        for i in range(max_attempts+1):
            try : 
        
                evaluation_results, _ = listingGenerationAgent().get_completion_from_model(evaluation_prompt)

                evaluation_results = evaluation_results.replace("```json", "").replace("```", "").strip()
                evaluation_results = json.loads(evaluation_results)

                logger.info(f"Evaluation results : {evaluation_results}")
                if evaluation_results["accepted"] == True:
                    logger.info("Postive : Listings accepted to be published")
                    logger.info(f"Reason : {evaluation_results['reason']}")
                else :
                    logger.info("Negative : Listings were rejected by model")
                    logger.info(f"Reason : {evaluation_results['reason']}")

                return evaluation_results
            
            except Exception as e: 
                logger.info(f"Failed to get a valid evaluation response from model at attempt : {i}, error : {e}")
                if i == max_attempts:
                    raise ValueError(f"Failed to get a valid evaluation response from model after {max_attempts} attempts.")
                logger.info("Retrying...")





    



