# Business rules engine
def evaluate_authorisation(minestar_data) -> bool:
    """Simple rule for now - expand as needed"""
    # Example:
    # if minestar_data["qualification_expired"]:
    #     return False
    return minestar_data.get("is_authorised", False)