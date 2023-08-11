class Bus:
    ID = 'id'
    LICENSE_PLATE = 'license_plate'
    TYPE = 'type'
    AMOUNT_SEATS = 'amount_seats'
    FIELDS = [LICENSE_PLATE, TYPE, AMOUNT_SEATS]

    def __init__(self, license_plate, type, amount_seats, id=None):
        self.id = id
        self.license_plate = license_plate
        self.type = type
        self.amount_seats = amount_seats

    def to_dict(self):
        return {
            self.ID: self.id,
            self.LICENSE_PLATE: self.license_plate,
            self.TYPE: self.type,
            self.AMOUNT_SEATS: self.amount_seats,
        }
