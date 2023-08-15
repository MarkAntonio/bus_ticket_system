from bus_ticket_system.app.util import BaseValidate
from .dao import SeatDao
from .model import Seat


class SeatBusiness(BaseValidate):

    def __init__(self):
        self.__seat_dao = SeatDao()

    def save(self, data):
        seat = self.__seat_dao.save(Seat(**data))  # atribui o id para eu retornar para a API
        return seat

    def get(self, **kwargs):
        if kwargs.get('bus_id'):
            return self.__seat_dao.get_all(kwargs['bus_id'])
        elif kwargs.get('id'):
            return self.__seat_dao.get_by_id(kwargs['id'])
        raise Exception('Field not exists')  # caso o programador coloque um campo que não existe ou está incorreto

    def update(self, current_seat, new_seat):
        new_seat.id = current_seat.id
        self.__seat_dao.update(current_seat, new_seat)

    def delete(self, bus_id):
        self.__seat_dao.delete_all(bus_id)

    def reconnect(self):
        self.__seat_dao.rollback()

    def _validate_is_free(self, string:str):
        if not string.upper() == 'TRUE' or 'FALSE':
            return 'The field is_free must contain only the word TRUE or FALSE'

