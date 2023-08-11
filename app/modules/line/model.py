from datetime import datetime, time


class Line:

    ID = 'id'
    ORIGIN = 'origin'
    DESTINATION = 'destination'
    DEPARTURE_TIME = 'departure_time'
    ARRIVAL_TIME = 'arrival_time'
    TOTAL_PRICE = 'total_price'
    FIELDS = [ORIGIN, DESTINATION, DEPARTURE_TIME, ARRIVAL_TIME, TOTAL_PRICE]

    _HOUR_FORMAT = '%H:%M'

    def __init__(self, origin: str, destination: str,
                 departure_time: time, arrival_time: time, total_price: str, id=None):
        self.id = id
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.total_price = total_price

    @classmethod
    def str_to_time(cls, value: str) -> time:
        return datetime.strptime(value, cls._HOUR_FORMAT).time()

    @classmethod
    def time_to_str(cls, value: time) -> str:
        return value.strftime(cls._HOUR_FORMAT)

    def to_dict(self):
        return {
            self.ID: self.id,
            self.ORIGIN: self.origin,
            self.DESTINATION: self.destination,
            self.DEPARTURE_TIME: self.time_to_str(self.departure_time),
            self.ARRIVAL_TIME: self.time_to_str(self.arrival_time),
            self.TOTAL_PRICE: self.total_price
        }
