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
            print(kwargs.get('number'))
            if kwargs.get('number'):
                return self.__seat_dao.get_by_number(kwargs['number'], kwargs['bus_id'])
            return self.__seat_dao.get_all(kwargs['bus_id'])

        raise Exception('Field not exists')  # caso o programador coloque um campo que não existe ou está incorreto

    def update(self, current_seat, new_seat):
        new_seat.number = current_seat.number
        self.__seat_dao.update(current_seat, new_seat)

    def delete(self, bus_id):
        self.__seat_dao.delete_all(bus_id)

    def reconnect(self):
        self.__seat_dao.rollback()

    def _validate_is_free(self, is_free:str):
        print(is_free.upper() != 'TRUE')
        if is_free.upper() != 'TRUE' and is_free.upper() != 'FALSE':
            return 'The field is_free must contain only the word TRUE or FALSE'

    # não preciso validar number, pois será incrementado pelo sistema. Logo não deve ter erros.