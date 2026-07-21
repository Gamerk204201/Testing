# Operator domain model
class Operator:
    def __init__(self, employee_id: str, name: str = None):
        self.employee_id = employee_id
        self.name = name   # ← Optional, fill if needed

    # Add operator validation rules here