from app.util import BaseDAO
from .model import Seat
from .sql import SqlSeat


class SeatDao(BaseDAO):


    def save(self, seat: Seat):
        cursor = self.connection.cursor()
        cursor.execute(SqlSeat._INSERT,
                       (seat.id,
                        seat.number,
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
            seats.append(self._create_object(columns_name, row, Seat))

        cursor.close()
        if seats:
            return seats

    def get_by_id(self, id: str):
        cursor = self.connection.cursor()
        cursor.execute(SqlSeat._SELECT_BY_ID.format(SqlSeat.TABLE_NAME, id))
        row = cursor.fetchone()
        if row:
            columns_name = [desc[0] for desc in cursor.description]
            cursor.close()
            seat = self._create_object(columns_name, row, Seat)
            return seat

    def update(self, current_seat: Seat, new_seat: Seat):
        cursor = self.connection.cursor()
        cursor.execute(SqlSeat._UPDATE.format(SqlSeat.TABLE_NAME),
                       (
                           new_seat.is_free,
                           new_seat.vacant_in,
                           str(current_seat.id)
                       ))
        self.connection.commit()
        cursor.close()

    # delete não está sendo usado, pois quando eu deleto um Bus ele deleta em cascade todos os Seats que tem o mesmo
    # bus_id do bus

