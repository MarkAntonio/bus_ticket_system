import re

from app.util import BaseValidate
from .dao import TicketDao
from .model import Ticket


class TicketBusiness(BaseValidate):
    _MONEY_REGEX = re.compile(r'^\d+(\.\d{2})?$')

    def __init__(self):
        self.__ticket_dao = TicketDao()

    def save(self, data):
        # convertendo a data para o tipo datetime
        ticket = self.__ticket_dao.save(Ticket(**data))  # atribui o id para eu retornar para a AP
        return ticket

    def get(self, **kwargs):
        if not kwargs:
            return self.__ticket_dao.get_all()
        elif kwargs.get('id'):
            return self.__ticket_dao.get_by_id(kwargs['id'])
        raise Exception('Field not exists')  # caso o programador coloque um campo que não existe ou está incorreto

    def update(self, current_ticket: Ticket, new_ticket: Ticket):
        self.__ticket_dao.update(current_ticket, new_ticket)

    def delete(self, id):
        self.__ticket_dao.delete(id)

    def _validate_total_price(self, price: str):
        if not self._MONEY_REGEX.match(price):
            return "The total price format is incorrect. Try a value such as 28.00, 159.99 and so on."
        if not float(price) > 0:
            return "The total price must be greater than 0."

    def _validate_bus_id(self, bus_id: str):
        if not bus_id.isnumeric():
            return 'Bus id must be a number.'

    def _validate_line_id(self, line_id: str):
        if not line_id.isnumeric():
            return 'Line id must be a number.'

    def reconnect(self):
        self.__ticket_dao.rollback()
