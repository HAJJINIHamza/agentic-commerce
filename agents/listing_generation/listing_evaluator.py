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
        logger.info("Evaluating generated listings...")
        evaluation_prompt = self.build_evaluation_prompt(product_name, 
                                                        product_category,
                                                        forbidden_claims,
                                                        title,
                                                        keywords,
                                                        description)
        
        evaluation_results, _ = listingGenerationAgent().get_completion_from_model(evaluation_prompt)

        for i in range(max_attempts+1):
            try : 
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



if __name__ == "__main__":
    product_name = "Sheet mask"
    product_category = "K-beauty, Sheet mask"
    forbidden_claims = ["Cures skin", "Instant results"]
    title = "[ARUMVIT] Collagen Moisturizing Sheet Mask – Charcoal Powder 10ppm, 15‑Minute Instant Hydration for All Skin Types, New Arrival Korean Skincare"
    keywords = """[Korean sheet mask, 
            charcoal face mask, 
            collagen mask, 
            moisturizing mask,
            nourishing mask, 
            face sheet mask, 
            skincare, beauty, 
            K-beauty, 
            all skin types, 
            instant effect, 
            15 minutes, 
            hydrating, 
            soothing, 
            firming, 
            aloe vera, 
            green tea, 
            hyaluronic acid, 
            charcoal powder ]
            """
    description = """
            Korean Beauty
            ARUMVIT OEM Korean sheet mask delivers a fast, 15‑minute boost of deep moisture and nourishment. 
            Infused with charcoal powder, collagen, aloe vera, green tea extract and hyaluronic acid, the mask helps soothe, hydrate and firm all skin types for a refreshed, radiant look. 
            Made in Korea with 100% natural‑derived ingredients, it is gentle enough for sensitive skin and provides an instant, non‑sticky finish that leaves skin feeling soft and supple.
                """
    listing_evaluator_agent = listingEvaluatorAgent()
    evaluation_results = listing_evaluator_agent.evaluate_listings(product_name, 
                                                                    product_category,
                                                                    forbidden_claims,
                                                                    title,
                                                                    keywords,
                                                                    description)
    print (f"This is a negative example. Model evaluation results is : {evaluation_results}")


    



