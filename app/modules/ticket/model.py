class Ticket:
    ID = 'id'
    TRIP_ID = 'trip_id'
    ORIGIN_ID = 'origin_id'
    DESTINATION_ID = 'destination_id'
    PASSENGER_ID = 'passenger_id'
    SEAT_ID = 'seat_id'
    ROUTE_PRICE = 'route_price'
    # Como o route_price é incrementado automaticamente pelo sistema através do cáculo entre a Route e a Line
    # Então ele não é um campo obrigatório.
    FIELDS = [TRIP_ID, ORIGIN_ID, DESTINATION_ID, PASSENGER_ID, SEAT_ID]

    def __init__(self, trip_id, origin_id, destination_id, passenger_id, seat_id, route_price: str, id=None):
        self.id = id
        self.trip_id = trip_id
        self.origin_id = origin_id
        self.destination_id = destination_id
        self.passenger_id = passenger_id
        self.seat_id = seat_id
        self.route_price = route_price

    def to_dict(self):
        return {
            self.ID: self.id,
            self.TRIP_ID: self.trip_id,
            self.ORIGIN_ID: self.origin_id,
            self.DESTINATION_ID: self.destination_id,
            self.PASSENGER_ID: self.passenger_id,
            self.SEAT_ID: self.seat_id,
            self.ROUTE_PRICE: f'{self.route_price:.2f}',
        }
