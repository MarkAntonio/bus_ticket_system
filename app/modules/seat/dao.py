from bus_ticket_system.app.database import ConnectDataBase
from .model import Seat
from .sql import SqlSeat


class SeatDao:

    def __init__(self):
        self.connection = ConnectDataBase().get_instance()

    def save(self, seat: Seat):
        cursor = self.connection.cursor()
        cursor.execute(SqlSeat._INSERT,
                       (seat.number,
                        seat.is_free,
                        seat.vacant_in,
                        seat.bus_id)
                       )
        self.connection.commit()
        cursor.close()
        return seat

    def get_all(self, bus_id):
        seats = []
        cursor = self.connection.cursor()
        cursor.execute(SqlSeat._SELECT_ALL.format(SqlSeat.TABLE_NAME, bus_id))
        result = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]

        for row in result:
            seats.append(self._create_object(columns_name, row))

        cursor.close()
        if seats:
            return seats

    def get_by_number(self, number, bus_id):
        cursor = self.connection.cursor()
        cursor.execute(SqlSeat._SELECT_BY_NUMBER.format(SqlSeat.TABLE_NAME, number, bus_id))
        row = cursor.fetchone()
        if row:
            columns_name = [desc[0] for desc in cursor.description]
            cursor.close()
            seat = self._create_object(columns_name, row)
            return seat

    def update(self, current_seat: Seat, new_seat: Seat):
        cursor = self.connection.cursor()
        cursor.execute(SqlSeat._UPDATE.format(SqlSeat.TABLE_NAME), (
            new_seat.is_free,
            new_seat.vacant_in,
            str(current_seat.number)))
        self.connection.commit()
        cursor.close()

    def delete_all(self, bus_id: int):
        cursor = self.connection.cursor()
        cursor.execute(SqlSeat._DELETE.format(SqlSeat.TABLE_NAME, bus_id))
        self.connection.commit()
        cursor.close()

    def _create_object(self, columns_name, data):
        if data:
            data = dict(zip(columns_name, data))
            seat = Seat(**data)
            return seat
        return None

    def rollback(self):
        self.connection.rollback()
