from app.database import ConnectDataBase
from .model import Passenger
from .sql import SqlPassenger
from app.util import BaseDAO


class PassengerDao(BaseDAO):

    def save(self, passenger: Passenger):
        cursor = self._save(SqlPassenger._INSERT,
                            (passenger.name,
                             passenger.phone)
                            )
        passenger.id = cursor.fetchone()[0]
        cursor.close()
        return passenger

    def get_all(self):
        return self._get_all(SqlPassenger._SELECT_ALL, Passenger)

    def get_by_id(self, id: int):
        return self._get_by(SqlPassenger._SELECT_BY_ID.format(SqlPassenger.TABLE_NAME, id), Passenger)

    def update(self, current_passenger: Passenger, new_passenger: Passenger):
        self._update(SqlPassenger._UPDATE.format(SqlPassenger.TABLE_NAME),
                     (
                         new_passenger.name,
                         new_passenger.phone,
                         str(current_passenger.id)
                     ))

    def delete(self, id: int):
        self._delete(SqlPassenger._DELETE.format(SqlPassenger.TABLE_NAME, id))
