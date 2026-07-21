# Authorisation rules
class Authorisation:
    def __init__(self, vehicle, operator, is_authorised: bool, reason: str = ""):
        self.vehicle = vehicle
        self.operator = operator
        self.is_authorised = is_authorised
        self.reason = reason

    def should_enable_competency(self) -> bool:
        """Core business rule"""
        return self.is_authorised