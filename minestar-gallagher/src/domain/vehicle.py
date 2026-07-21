# Vehicle domain model
class Vehicle:
    def __init__(self, call_sign: str, gallagher_cardholder_id: str = None):
        self.call_sign = call_sign
        self.gallagher_cardholder_id = gallagher_cardholder_id   # ← Map from your data

    # Add any vehicle-specific logic here later