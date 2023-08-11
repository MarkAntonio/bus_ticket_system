import re

from .dao import LineDao
from .model import Line
from bus_ticket_system.app.util import BaseValidate


class LineBusiness(BaseValidate):
    # Expressão regular para identificar padrão de horas
    _TIME_REGEX = re.compile(r'^(?:[01]\d|2[0-3]):[0-5]\d$')
    # \d - Indica que é qualquer dígito
    # [0-5] - Limita os valores de 0 a 5
    # (?: ... ) - é um grupo não capturador que permite agrupar as alternativas.
    # | -  é um operador de alternância.
    # 2[0-3] - captura horas de 20 a 23
    # [01]\d - captura horas de 00 a 19.

    _MONEY_REGEX = re.compile(r'^\d+(\.\d{2})?$')
    # \d+ - Indica que deve ter um ou mais dígitos. O + obriga que tenha pelo menos 1 dígito.
    # (\.\d{2})? - Indica que no final pode ou não ter um . e 2 dígitos
    # dessa forma aceitará valores como: 1, 20, 25.99 etc. O Banco de dados transformará de 2 para 2.00


    def __init__(self):
        self.__line_dao = LineDao()

    def save(self, data):
        line = self.__line_dao.save(Line(**data))  # atribui o id para eu retornar para a API
        return line

    def get(self, **kwargs):
        if not kwargs:
            return self.__line_dao.get_all()
        elif kwargs.get('id'):
            return self.__line_dao.get_by_id(kwargs['id'])
        raise Exception('Field not exists')  # caso o programador coloque um campo que não existe ou está incorreto

    def update(self, current_line, new_line):
        self.__line_dao.update(current_line, new_line)

    def delete(self, id):
        self.__line_dao.delete(id)

    def reconnect(self):
        self.__line_dao.rollback()

    def _validate_arrival_time(self, arrival):
        if not self._TIME_REGEX.match(arrival):
            return "The arrival time is incorrect. Try a hour format such as 18:46, 05:16 and so on."

    def _validate_departure_time(self, departure):
        if not self._TIME_REGEX.match(departure):
            return "The departure time is incorrect. Try a hour format such as 18:46, 05:16 and so on."


    def _validate_total_price(self, price: str): # 18.00 | 145.98
        if not self._MONEY_REGEX.match(price):
            return "The total price format is incorrect. Try a value such as 28.00, 159.99 and so on."
        if not float(price) > 0:
            return "The total price must be greater than 0."
