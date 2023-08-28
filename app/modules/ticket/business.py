import re

from app.util import BaseValidate
from .dao import TicketDao
from .model import Ticket
from app.modules.line import Line
from app.modules.trip import Trip

class TicketBusiness(BaseValidate):
    _MONEY_REGEX = re.compile(r'^\d+(\.\d{2})?$')

    def __init__(self):
        self.__ticket_dao = TicketDao()

    def save(self, data):
        ticket = self.__ticket_dao.save(Ticket(**data))  # atribui o id para eu retornar para a AP
        return ticket


    def get(self, **kwargs):
        if not kwargs:
            return self.__ticket_dao.get_all()
        elif kwargs.get(Ticket.ID):
            return self.__ticket_dao.get_by_id(kwargs[Ticket.ID])
        raise Exception('Field not exists')  # caso o programador coloque um campo que não existe ou está incorreto

    def see_ticket(self, id):
        data = self.__ticket_dao.get_join(id)
        # convertendo a data
        data['date'] = Trip.datetime_to_str(data['date'])
        # convertendo a hora
        data['time'] = Line.time_to_str(data['time'])
        # criando a key line com a junção da line_origin e line_destination e deletando-as
        data['line'] = data['line_origin'] + ' - ' + data['line_destination']
        data.pop('line_origin')
        data.pop('line_destination')
        return data
    def update(self, current_ticket: Ticket, new_ticket: Ticket):
        self.__ticket_dao.update(current_ticket, new_ticket)

    def delete(self, id):
        self.__ticket_dao.delete(id)

    def _validate_trip_id(self, trip_id: str):
        if not trip_id.isnumeric():
            return 'Trip id must be a number.'

    def _validate_origin_id(self, origin_id: str):
        if not origin_id.isnumeric():
            return 'Origin id must be a number.'

    def _validate_destination_id(self, destination_id: str):
        if not destination_id.isnumeric():
            return 'Destination id must be a number.'

    def _validate_passenger_id(self, passenger_id: str):
        if not passenger_id.isnumeric():
            return 'Passenger id must be a number.'

    def reconnect(self):
        self.__ticket_dao.rollback()
