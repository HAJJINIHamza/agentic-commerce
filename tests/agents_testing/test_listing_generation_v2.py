from agents.listing_generation.listing_generator import listingGenerationAgent

def test_generate_product_title():
    product_id="7"
    product_name="Facial sheet mask, Anua - Kpop Demon Hunters Vita C Porestrix Brightening Serum Mask"
    product_category="Beauty > Skincare > Face Mask & Packs"
    product_details="""
                    1- Major Ingredients:
                    Water,Hippophae Rhamnoides Water,Butylene Glycol,Propanediol,Glycerin,Niacinamide,1,2-Hexanediol,Isopentyldiol,Trehalose,Arginine,Carbomer,Allantoin,Dipotassium Glycyrrhizate,Panthenol,Polyglyceryl-10 Laurate,Xanthan Gum,Ethylhexylglycerin,Adenosine,Ascorbyl Glucoside,3-O-Ethyl Ascorbic Acid,Sodium Ascorbyl Phosphate,Disodium EDTA,Glyceryl Acrylate/Acrylic Acid Copolymer,Melia Azadirachta Flower Extract,Ocimum Sanctum Leaf Extract,Melia Azadirachta Leaf Extract,Citrus Limon (Lemon) Peel Oil,Curcuma Longa (Turmeric) Root Extract,Corallina Officinalis Extract,Glutathione,Ascorbic Acid,Coco-Caprylate/Caprate,Hydrogenated Lecithin,Pentylene Glycol,Polyglyceryl-10 Oleate,Sodium Surfactin,Hydroxypropyl Cyclodextrin,Collagen,Dipeptide-15,Tannic Acid,Polysorbate 20,Tripeptide-1,Anemarrhena Asphodeloides Root Extract,Cysteine,Thioctic Acid,Hexapeptide-9,Palmitoyl Pentapeptide-4,Palmitoyl Tripeptide-5,Palmitoyl Tetrapeptide-7,Sodium Acetyl sh-Oligopeptide-195 SP Lysine N6-(Succinimidopropionyl Thioethyl Dipalmitoyl Glycerophosphate),Sodium Phenylbutyroyl Histidinyl 4-t-Butyl D-Phenylalanyl Arginyl Lysine N6-(Succinimidopropionyl Thioethyl Dipalmitoyl Glycerophosphate),Limonene.

                    2- Benefits:
                    * This mask is packed with rich serum to help brighten the skin tone and minimize the appearance of pores.
                    * Formulated with Vitamin C, Porestrix™ and MELA-LIPO 4™ to tone up the complexion, tighten pores, and refine skin texture.
                    * Features Anua's patented brightening-targeted liposome, MELA-LIPO 4™, which combines Ascorbyl Glucoside, Thioctic Acid, Glutathione, and Cysteine to care for pores while enhancing skin radiance.

                    3- How to use:
                    After toning, leave the mask on for around 10 to 20 minutes and lightly pat to aid absorption of the remaining essence after removing it.
                    """
    agent = listingGenerationAgent()
    #list_of_titles = get_product_titles_from_page(product_id, 
    #                                              product_name)

    #title_generation_prompt = agent.get_predifined_prompts()
    #title_generation_prompt = agent.build_title_generation_prompt(title_generation_prompt, 
    #                                                               product_name,
    #                                                               product_category,
    #                                                               product_details,
    #                                                               list_of_titles)

    title = agent.generate_product_title(
                                        product_id,
                                        product_name,
                                        product_category,
                                        product_details
                                        )

    return title

if __name__ == "__main__":
    title = test_generate_product_title()
    print(f"Generated title: {title}")