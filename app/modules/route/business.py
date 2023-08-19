import re

from bus_ticket_system.app.util import BaseValidate
from .dao import RouteDao
from .model import Route


class RouteBusiness(BaseValidate):
    # Expressão regular para identificar padrão de número de telefone
    _PHONE_REGEX = re.compile(r'\(\d{2}\)9\d{4}-\d{4}$')

    def __init__(self):
        self.__route_dao = RouteDao()

    def save(self, data):
        route = self.__route_dao.save(Route(**data))  # atribui o id para eu retornar para a API
        return route

    def get(self, **kwargs):
        if not kwargs:
            return self.__route_dao.get_all()
        elif kwargs.get('id'):
            return self.__route_dao.get_by_id(kwargs['id'])
        raise Exception('Field not exists')  # caso o programador coloque um campo que não existe ou está incorreto

    def update(self, current_route, new_route):
        new_route.id = current_route.id
        self.__route_dao.update(current_route, new_route)

    def delete(self, id):
        self.__route_dao.delete(id)

    def reconnect(self):
        self.__route_dao.rollback()

    def _validate_phone(self, phone):
        if not self._PHONE_REGEX.match(phone):
            return "The phone number is incorrect. Try a number format such as (xx)9xxxx-xxxx where x = digit."

