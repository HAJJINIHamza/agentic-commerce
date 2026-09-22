from agents.listing_generation.listing_evaluator import listingEvaluatorAgent

def negative_test_listing_evaluator():
    product_name = "Sheet mask"
    product_category = "K-beauty, Sheet mask"
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
            Made in Korea with 100% natural‑derived ingredients, it is gentle enough for sensitive skin and provides an instant outcomes that leaves skin feeling soft and supple.
                """
    listing_evaluator_agent = listingEvaluatorAgent()
    evaluation_results = listing_evaluator_agent.evaluate_listings(product_name, 
                                                                    product_category,
                                                                    title,
                                                                    keywords,
                                                                    description)
    print (f"This is a negative example. Model evaluation results is : {evaluation_results}")
    
    assert evaluation_results["accepted"] == False, "Evaluator has failed. Expected the listing to be rejected, but it was accepted. :("
    print ("TEST PASSED :)")

if __name__ == "__main__":
    negative_test_listing_evaluator()

