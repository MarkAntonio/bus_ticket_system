from datetime import datetime, time


class Seat:
    NUMBER = 'number'  # seat numbering, represents the seat
    IS_FREE = 'is_free'
    VACANT_IN = 'vacant_in'
    BUS_ID = 'bus_id'  # Foreign key
    FIELDS = [NUMBER, IS_FREE, VACANT_IN, BUS_ID]

    def __init__(self, is_free, number, vacant_in, bus_id):
        self.number = number
        self.is_free = is_free
        self.vacant_in = vacant_in
        self.bus_id = bus_id

    def to_dict(self):
        return {
            self.NUMBER: self.number,
            self.IS_FREE: self.is_free,
            self.VACANT_IN: self.vacant_in,
            self.BUS_ID: self.bus_id
        }
