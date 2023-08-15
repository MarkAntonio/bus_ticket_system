from datetime import datetime, time


class Passenger:
    ID = 'id'
    NAME = 'name'
    PHONE = 'phone'
    FIELDS = [NAME, PHONE]

    def __init__(self, name: str, phone: str, id=None):
        self.id = id
        self.name = name
        self.phone = phone

    def to_dict(self):
        return {
            self.ID: self.id,
            self.NAME: self.name,
            self.PHONE: self.phone
        }
