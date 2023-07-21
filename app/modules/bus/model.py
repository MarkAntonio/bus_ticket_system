class Bus:

    FIELDS_TO_VALIDATE = ['id', 'license_plate', 'type', 'amount_seats']

    def __init__(self, license_plate, type, amount_seats, id=None):
        self.id = id
        self.license_plate = license_plate
        self.type = type
        self.amount_seats = amount_seats

    def to_dict(self):
        return {str(col): getattr(self, col) for col in self.FIELDS_TO_VALIDATE}
