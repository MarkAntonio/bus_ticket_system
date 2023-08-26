class Ticket:
    ID = 'id'
    ROUTE_PRICE = 'route_price'
    PASSENGER_ID = 'passenger_id'
    TRIP_ID = 'trip_id'
    SEAT_ID = 'seat_id'
    # Como o route_price é incrementado automaticamente pelo sistema através do cáculo entre a Route e a Line
    # Então ele não é um campo obrigatório.
    FIELDS = [PASSENGER_ID, TRIP_ID, SEAT_ID]

    def __init__(self, route_price, passenger_id, trip_id, seat_id, id=None):
        self.id = id
        self.route_price = route_price
        self.passenger_id = passenger_id
        self.trip_id = trip_id
        self.seat_id = seat_id

    def to_dict(self):
        return {
            self.ID: self.id,
            self.ROUTE_PRICE: self.route_price,
            self.PASSENGER_ID: self.passenger_id,
            self.trip_id: self.trip_id,
            self.SEAT_ID: self.seat_id
        }
