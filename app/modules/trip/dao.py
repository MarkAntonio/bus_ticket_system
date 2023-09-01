from app.util import BaseDAO
from .model import Trip
from .sql import SqlTrip


class TripDao(BaseDAO):

    def save(self, trip: Trip):
        cursor = self.connection.cursor()
        cursor.execute(SqlTrip._INSERT,
                       (
                        Trip.datetime_to_str(trip.date),
                        trip.line_id,
                        trip.bus_id)
                       )
        self.connection.commit()
        trip.id = cursor.fetchone()[0]
        cursor.close()
        return trip

    def get_all(self):
        trips = []
        cursor = self.connection.cursor()
        cursor.execute(SqlTrip._SELECT_ALL)
        result = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]

        for row in result:
            trips.append(self._create_object(columns_name, row, Trip))

        cursor.close()
        if trips:
            return trips

    def get_by_id(self, id: int):
        cursor = self.connection.cursor()
        cursor.execute(SqlTrip._SELECT_BY_ID.format(SqlTrip.TABLE_NAME, id))
        row = cursor.fetchone()
        if row:
            columns_name = [desc[0] for desc in cursor.description]
            cursor.close()
            trip = self._create_object(columns_name, row, Trip)
            return trip

    def update(self, current_trip: Trip, new_trip: Trip):
        cursor = self.connection.cursor()
        cursor.execute(SqlTrip._UPDATE.format(SqlTrip.TABLE_NAME),
                       (
                           Trip.datetime_to_str(new_trip.date),
                           new_trip.line_id,
                           new_trip.bus_id,
                           str(current_trip.id)
                       ))
        self.connection.commit()
        cursor.close()

    def delete(self, id: int):
        cursor = self.connection.cursor()
        cursor.execute(SqlTrip._DELETE.format(SqlTrip.TABLE_NAME, id))
        self.connection.commit()
        cursor.close()
