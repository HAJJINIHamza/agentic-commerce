from agents.listing_generation.listing_generator import listingGenerationAgent

target_country = "Taiwan"
product_name = "Korean Cooling Scalp Brush"
product_category = "Hair care accessory"
main_benefit = "Helps daily scalp massage during shower"
buyer_persona = "young female buyer interested in K-beauty" 
forbidden_claims = "hair-loss cure, medical treatment, disease cure"


def test_listing_generation():

    listings, tiktok_listings = listingGenerationAgent().generate_listings(target_country,
                                               product_name,
                                               product_category,
                                               main_benefit,
                                               buyer_persona,
                                               forbidden_claims
                                               )
    
    return listings, tiktok_listings


    
if __name__ == "__main__":
    listings, tiktok_listings = test_listing_generation()
    print("Listings : ")
    print (listings)
    print (tiktok_listings) 