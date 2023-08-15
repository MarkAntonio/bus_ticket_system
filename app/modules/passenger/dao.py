from bus_ticket_system.app.database import ConnectDataBase
from .model import Passenger
from .sql import SqlPassenger


class PassengerDao:

    def __init__(self):
        self.connection = ConnectDataBase().get_instance()

    def save(self, passenger: Passenger):
        cursor = self.connection.cursor()
        cursor.execute(SqlPassenger._INSERT,
                       (passenger.name,
                        passenger.phone)
                       )
        self.connection.commit()
        passenger.id = cursor.fetchone()[0]
        cursor.close()
        return passenger

    def get_all(self):
        passengers = []
        cursor = self.connection.cursor()
        cursor.execute(SqlPassenger._SELECT_ALL)
        result = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]

        for row in result:
            passengers.append(self._create_object(columns_name, row))

        cursor.close()
        if passengers:
            return passengers

    def get_by_id(self, id: int):
        cursor = self.connection.cursor()
        cursor.execute(SqlPassenger._SELECT_BY_ID.format(SqlPassenger.TABLE_NAME, id))
        row = cursor.fetchone()
        if row:
            columns_name = [desc[0] for desc in cursor.description]
            cursor.close()
            passenger = self._create_object(columns_name, row)
            return passenger

    def update(self, current_passenger: Passenger, new_passenger: Passenger):
        cursor = self.connection.cursor()
        cursor.execute(SqlPassenger._UPDATE.format(SqlPassenger.TABLE_NAME), (
            new_passenger.name,
            new_passenger.phone,
            str(current_passenger.id)))
        self.connection.commit()
        cursor.close()

    def delete(self, id: int):
        cursor = self.connection.cursor()
        cursor.execute(SqlPassenger._DELETE.format(SqlPassenger.TABLE_NAME, id))
        self.connection.commit()
        cursor.close()

    def _create_object(self, columns_name, data):
        if data:
            data = dict(zip(columns_name, data))
            passenger = Passenger(**data)
            return passenger
        return None

    def rollback(self):
        self.connection.rollback()
