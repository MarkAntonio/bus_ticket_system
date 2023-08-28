from app.util import BaseValidate
from .dao import SeatDao
from .model import Seat
from ..bus import Bus


class SeatBusiness(BaseValidate):
    __tag_is_free = True

    def __init__(self):
        self.__seat_dao = SeatDao()

    def save(self, data):
        seat = self.__seat_dao.save(Seat(**data))  # atribui o id para eu retornar para a API
        return seat

    def get(self, **kwargs):
        if kwargs.get(Seat.BUS_ID):
            return self.__seat_dao.get_all(kwargs[Seat.BUS_ID])
        if kwargs.get(Seat.ID):
            return self.__seat_dao.get_by_id(kwargs[Seat.ID])

        raise Exception('Field not exists')  # caso o programador coloque um campo que não existe ou está incorreto

    def update(self, current_seat, new_seat):
        new_seat.number = current_seat.number
        self.__seat_dao.update(current_seat, new_seat)

    def delete(self, bus_id):
        self.__seat_dao.delete_all(bus_id)

    def reconnect(self):
        self.__seat_dao.rollback()

    def _validate_is_free(self, is_free: str):
        if is_free.upper() != 'TRUE' and is_free.upper() != 'FALSE':
            return 'The field is_free must contain only the word TRUE or FALSE'
        if is_free.upper() == 'FALSE':
            self.__tag_is_free = False
        else:
            self.__tag_is_free = True

    def _validate_vacant_in(self, vacant_in: str):
        if vacant_in.upper() == 'NULL' and not self.__tag_is_free:
            return 'The seat is not FREE, so, the field vacant_in must be not NULL.'

    # não preciso validar number nem o bus_id, pois será incrementado pelo sistema. Logo não deve ter erros.
