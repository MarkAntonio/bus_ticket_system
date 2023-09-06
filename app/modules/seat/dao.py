from app.util import BaseDAO
from .model import Seat
from .sql import SqlSeat


class SeatDao(BaseDAO):

    # O save somente é acessado pelo Bus Business
    def save(self, seat: Seat):
        cursor = self._save(SqlSeat._INSERT,
                       (seat.id,
                        seat.number,
                        seat.is_free,
                        seat.vacant_in,
                        seat.bus_id)
                       )
        cursor.close()
        return seat

    def get_all(self, bus_id):
        return self._get_all(SqlSeat._SELECT_ALL.format(SqlSeat.TABLE_NAME, bus_id), Seat)

    def get_by_id(self, id:str):
        return self._get_by(SqlSeat._SELECT_BY_ID.format(SqlSeat.TABLE_NAME, id), Seat)

    def update(self, current_seat: Seat, new_seat: Seat):
        self._update(SqlSeat._UPDATE.format(SqlSeat.TABLE_NAME),
                       (
                           new_seat.is_free,
                           new_seat.vacant_in,
                           str(current_seat.id)
                       ))

    # delete não está sendo usado, pois quando eu deleto um Bus ele deleta em cascade todos os Seats vinculados
