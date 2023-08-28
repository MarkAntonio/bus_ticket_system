import re
import traceback

from app.util import BaseValidate
from .dao import LineDao
from .model import Line
from app.modules.route.business import RouteBusiness
from app.modules.route import Route


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

    _route_business = RouteBusiness()

    def __init__(self):
        self.__line_dao = LineDao()

    def save(self, data):
        # tranformando as strings de hora em formato datetime.time para criar o objeto
        data[Line.DEPARTURE_TIME] = Line.str_to_time(data[Line.DEPARTURE_TIME])
        data[Line.ARRIVAL_TIME] = Line.str_to_time(data[Line.ARRIVAL_TIME])

        line = self.__line_dao.save(Line(**data))  # atribui o id para eu retornar para a API
        try:
            self.__create_initial_routes(line)
        except Exception as exception:
            traceback.print_exc()
            raise exception
        return line

    def __create_initial_routes(self, line: Line):
        # criando rota inicial
        inicial_route = self._route_business.save(
            {
                Route.CITY: line.origin,
                Route.TIME: Line.time_to_str(line.departure_time),
                Route.PRICE: '0.00',
                Route.LINE_ID: line.id
            }
        )
        # criando a rota final
        final_route = self._route_business.save(
            {
                Route.CITY: line.destination,
                Route.TIME: Line.time_to_str(line.arrival_time),
                Route.PRICE: line.total_price,
                Route.LINE_ID: line.id
            }
        )
        if not inicial_route or not final_route:
            raise Exception

    def get(self, **kwargs):
        if not kwargs:
            return self.__line_dao.get_all()
        elif kwargs.get(Line.ID):
            return self.__line_dao.get_by_id(kwargs[Line.ID])
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

    def _validate_total_price(self, price: str):
        if not self._MONEY_REGEX.match(price):
            return "The total price format is incorrect. Try a value such as 28.00, 159.99 and so on."
        if not float(price) > 0:
            return "The total price must be greater than 0."
