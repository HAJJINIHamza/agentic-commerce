from agents.listing_generation.listing_evaluator import listingEvaluatorAgent

product_name = "Korean Cooling Scalp Brush"
product_category = "Hair care accessory"
forbidden_claims = "hair-loss cure, medical treatment, disease cure"
title = "Korean Cooling Scalp Massage Brush - Refreshing Head Spa for Daily Hair Care & Deep Cleansing"
keywords = [
    "K-beauty",
    "scalp massager",
    "hair care",
    "cooling brush",
    "scalp care",
    "shampoo brush",
    "Korean beauty",
    "scalp massage",
    "head spa",
    "hair accessory"
  ]
description =  [
    "✨ Experience the ultimate K-beauty head spa right in your own shower! Our Korean Cooling Scalp Brush transforms your daily hair wash into a professional relaxation ritual.",
    "❄️ Instant Refreshment: Experience a soothing cooling sensation that awakens your senses and refreshes your scalp instantly.",
    "🧼 Enhanced Deep Cleansing: Gently exfoliates the scalp and helps remove impurities and excess oil more effectively than using fingers alone, leaving your scalp feeling breathable and clean.",
    "💆‍♀️ Stress-Relieving Massage: The soft yet firm bristles provide a relaxing massage that helps relieve tension and promotes a sense of well-being after a long day.",
    "🌸 Ergonomic Grip: Designed to fit perfectly in your hand, making it easy and comfortable to use during your shampooing routine.",
    "✨ The Perfect Self-Care Addition: A must-have accessory for any K-beauty enthusiast looking to elevate their hair care game."
  ]
safe_claims = [
    "Promotes a feeling of freshness and cleanliness",
    "Provides a relaxing and soothing scalp massage experience",
    "Assists in removing surface impurities during shampooing",
    "Ergonomic design for a comfortable user experience"
  ]
tiktok_hook = "POV: You just upgraded your shower routine with this K-beauty secret! 🛁✨",
tiktok_short_video_script = \
"""
[0-3s] Visual: Fast cuts of an aesthetic bathroom and a close-up of the Korean Cooling Scalp Brush. 
Text overlay: 'Shower Game Changer 🫧'. Audio: 'Ever feel like your scalp needs a little extra love?'\n[3-8s] Visual: User applying shampoo and using the brush in gentle circular motions on the scalp. 
Audio: 'This Korean Cooling Scalp Brush makes every shower feel like a professional spa day.'\n[8-12s] Visual: Close-up of the brush bristles and the user looking relaxed/refreshed. Text overlay: 'Refreshing & Relaxing ❄️'. Audio: 'It's the ultimate way to unwind and refresh your scalp after a long day.'\n[12-15s] Visual: Product shot with a 'Shop Now' button and Shopee logo. Audio: 'Level up your K-beauty routine! Grab yours on Shopee today! ✨'"
"""

def test_listing_evaluator(product_name, 
                            product_category,
                            forbidden_claims,
                            title,
                            keywords,
                            description,
                            safe_claims,
                            tiktok_hook,
                            tiktok_short_video_script):        
    eval_results = listingEvaluatorAgent().evaluate_listings(product_name, 
                                                                product_category,
                                                                forbidden_claims,
                                                                title,
                                                                keywords,
                                                                description,
                                                                safe_claims,
                                                                tiktok_hook,
                                                                tiktok_short_video_script)

    return eval_results 


if __name__ == "__main__":
    eval_results = test_listing_evaluator(product_name, 
                                            product_category,
                                            forbidden_claims,
                                            title,
                                            keywords,
                                            description,
                                            safe_claims,
                                            tiktok_hook,
                                            tiktok_short_video_script)
    print("Results : ", eval_results)
