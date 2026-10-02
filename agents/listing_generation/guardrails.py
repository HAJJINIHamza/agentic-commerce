import yaml

#############################################
# Guardrails for Shopee listings
#############################################

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

forbidden_claims = config["listing_generation"]["forbidden_claims"]

def is_safe_from_forbidden_claims(description : str):
    """
    Verify if an item of the list of forbidden claims exist in description
    """

    for claim in forbidden_claims:
        if claim in description :
            return {"is_safe": False, "forbidden_claim": claim}

    return {"is_safe": True, "forbidden_claim": None}

def is_title_length_acceptable(title: str):
    """
    Shopee title shouldn't surpass 180 character
    """
    length = len(title)
    if length <= 180:
        return True
    return False

def is_title_contains_kbeauty_keyword(title):
    """
    Verify that generated title contains Kbeauty keyword
    """
    kbeauty_keywords = ["kbeauty", "k-beauty", "korean beauty"]
    title = title.lower()

    for keyword in kbeauty_keywords:
        if keyword in title:
            return True

    return False

def is_description_length_acceptable(description: str):
    """
    Shopee description shouldn't surpass 5000 character
    """
    length = len(description)
    if length <= 5000:
        return True
    return False
