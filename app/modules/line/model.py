class Line:
    ORIGIN = 'origin'
    DESTINATION = 'destination'
    DEPARTURE_TIME = 'departure_time'
    ARRIVAL_TIME = 'arrival_time'
    TOTAL_PRICE = 'total_price'
    FIELDS = [ORIGIN, DESTINATION, DEPARTURE_TIME, ARRIVAL_TIME, TOTAL_PRICE]

    def __init__(self, origin: str, destination: str, departure_time, arrival_time, total_price: str, id=None):
        self.id = id
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.total_price = total_price
