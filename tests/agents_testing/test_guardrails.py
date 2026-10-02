from agents.listing_generation.guardrails import is_safe_from_forbidden_claims, is_title_length_acceptable, is_title_contains_kbeauty_keyword


forbidden_claims = ["cures acne",
                    "treats eczema / psoriasis / rosacea",
                    "prevents or reduces disease",
                    "diagnoses skin conditions", "FDA approved"]

description = """Korean Beauty
        ARUMVIT OEM Korean sheet mask delivers a fast, 15‑minute boost of deep moisture and nourishment, it cures acne as well. 
        Infused with charcoal powder, collagen, aloe vera, green tea extract and hyaluronic acid, the mask helps soothe, hydrate and firm all skin types for a refreshed, radiant look. 
        Made in Korea with 100% natural‑derived ingredients, it is gentle enough for sensitive skin and provides an instant outcomes that leaves skin feeling soft and supple."""

title = "Facial sheet mask, Anua - Kpop Demon Hunters Vita C Porestrix Brightening Serum Mask -- " \
"           Facial sheet mask, Anua - Kpop Demon Hunters Vita C Porestrix Brightening Serum Mask"

def test_is_safe_from_forbidden_claims():
    is_safe = is_safe_from_forbidden_claims(description)
    assert is_safe["is_safe"] == False, "Test failed because this is a negative example, description is not safe."

def test_is_title_length_acceptable():
    is_title_length = is_title_length_acceptable(title)
    assert is_title_length == False, "This is a negative example, this is a very long title." 

def test_is_title_contains_kbeauty_keyword():
    is_kbeauty = is_title_contains_kbeauty_keyword(title)
    assert is_kbeauty == False, "Negative example, title contains no kbeauty words." 

if __name__ == "__main__":
    test_is_safe_from_forbidden_claims()
    test_is_title_length_acceptable()
    test_is_title_contains_kbeauty_keyword()
    print ("ALL TESTS PASSED.")