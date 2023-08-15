import re  # Regular Expressions

from bus_ticket_system.app.util import BaseValidate
from .model import Bus
from .dao import BusDao


class BusBusiness(BaseValidate):
    # Expressão Regular para identificar padrão de placas de veículos brasileiras
    _LICENSE_REGEX = re.compile(r'^[A-Z]{3}\d[A-Z]\d{2}$')
    _AVAILABLE_TYPES = ('Convencional', 'Executivo', 'Leito', 'Leito Cama')

    def __init__(self):
        self.__bus_dao = BusDao()

    def save(self, data):
        bus = self.__bus_dao.save(Bus(**data))  # atribui o id para eu retornar para a API
        return bus

    def get(self, **kwargs):
        if not kwargs:
            return self.__bus_dao.get_all()
        elif kwargs.get('id'):
            return self.__bus_dao.get_by_id(kwargs['id'])
        elif kwargs.get('license_plate'):
            return self.__bus_dao.get_by_license(kwargs['license_plate'])
        elif kwargs.get('type'):
            return self.__bus_dao.get_all_by_type(kwargs['type'])
        raise Exception('Field not exists')  # caso o programador coloque um campo que não existe ou está incorreto

    def update(self, current_bus, new_bus):
        self.__bus_dao.update(current_bus, new_bus)

    def delete(self, id):
        self.__bus_dao.delete(id)


    def _validate_license_plate(self, license):
        if not self._LICENSE_REGEX.match(license):
            return "The license_plate format is incorrect. The format must have the following sequence: AAA9A99"
        if self.__bus_dao.get_by_license(license):
            return "There's already a registered bus with this license plate"

    def _validate_type(self, type):
        if type not in self._AVAILABLE_TYPES:
            return f"The type is incorrect. Try to put some of these: {self._AVAILABLE_TYPES}"
        return None

    def _validate_amount_seats(self, amount_seats):
        # todo valor sempre é recebido do request como string, por isso que eu posso usar o método isdigit()
        # para saber se só existem números nessa variável
        if not amount_seats.isdigit():
            return 'amount_seats must be a number of int type'
        return None

    def reconnect(self):
        self.__bus_dao.rollback()