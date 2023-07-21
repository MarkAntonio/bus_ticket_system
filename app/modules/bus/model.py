class Bus:

    FIELDS = ['license_plate', 'type', 'amount_seats']

    def __init__(self, license_plate, type, amount_seats, id=None):
        self.id = id
        self.license_plate = license_plate
        self.type = type
        self.amount_seats = amount_seats
