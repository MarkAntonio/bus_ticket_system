from app.util import BaseDAO
from .model import Trip
from .sql import SqlTrip


class TripDao(BaseDAO):

    def save(self, trip: Trip):
        cursor = self._save(SqlTrip._INSERT,
                            (
                                Trip.datetime_to_str(trip.date),
                                trip.line_id,
                                trip.bus_id
                            ))
        trip.id = cursor.fetchone()[0]
        cursor.close()
        return trip

    def get_all(self):
        return self._get_all(SqlTrip._SELECT_ALL, Trip)

    def get_by_id(self, id: int):
        return self._get_by(SqlTrip._SELECT_BY_ID.format(SqlTrip.TABLE_NAME, id), Trip)

    def update(self, current_trip: Trip, new_trip: Trip):
        self._update(SqlTrip._UPDATE.format(SqlTrip.TABLE_NAME),
                     (
                         Trip.datetime_to_str(new_trip.date),
                         new_trip.line_id,
                         new_trip.bus_id,
                         str(current_trip.id)
                     ))

    def delete(self, id: int):
        self._delete(SqlTrip._DELETE.format(SqlTrip.TABLE_NAME, id))
