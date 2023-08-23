import re

from app.util import BaseValidate
from .dao import RouteDao
from .model import Route


class RouteBusiness(BaseValidate):

    _TIME_REGEX = re.compile(r'^(?:[01]\d|2[0-3]):[0-5]\d$')
    _MONEY_REGEX = re.compile(r'^\d+(\.\d{2})?$')

    def __init__(self):
        self.__route_dao = RouteDao()

    def save(self, data):
        data[Route.TIME] = Route.str_to_time(data[Route.TIME])
        route = self.__route_dao.save(Route(**data))  # atribui o id para eu retornar para a API
        return route

    def get(self, **kwargs):
        if not kwargs:
            return self.__route_dao.get_all()
        if kwargs.get('id'):
            return self.__route_dao.get_by_id(kwargs['id'])
        if kwargs.get('line_id'):
            return self.__route_dao.get_all_by_line(kwargs['line_id'])

        raise Exception('Field not exists')  # caso o programador coloque um campo que não existe ou está incorreto

    def update(self, current_route: Route, new_route: Route):
        new_route.time = Route.str_to_time(new_route.time)
        self.__route_dao.update(current_route, new_route)

    def delete(self, id):
        self.__route_dao.delete(id)

    def reconnect(self):
        self.__route_dao.rollback()

    def _validate_time(self, time):
        if not self._TIME_REGEX.match(time):
            return "The time is incorrect. Try a hour format such as 18:46, 05:16 and so on."

    def _validate_price(self, price: str):
        if not self._MONEY_REGEX.match(price):
            return "The total price format is incorrect. Try a value such as 28.00, 159.99 and so on."
        if not float(price) > 0:
            return "The total price must be greater than 0."
