from app.database import ConnectDataBase
from .model import Ticket
from .sql import SqlTicket


class TicketDao:

    def __init__(self):
        self.connection = ConnectDataBase().get_instance()

    def save(self, ticket: Ticket):
        cursor = self.connection.cursor()
        cursor.execute(SqlTicket._INSERT,
                       (
                           ticket.trip_id,
                           ticket.origin_id,
                           ticket.destination_id,
                           ticket.passenger_id,
                           ticket.seat_id,
                           ticket.route_price
                       ))
        self.connection.commit()
        ticket.id = cursor.fetchone()[0]
        cursor.close()
        return ticket

    def get_all(self):
        tickets = []
        cursor = self.connection.cursor()
        cursor.execute(SqlTicket._SELECT_ALL)
        result = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]

        for row in result:
            tickets.append(self._create_object(columns_name, row))

        cursor.close()
        if tickets:
            return tickets

    def get_by_id(self, id: int):
        cursor = self.connection.cursor()
        cursor.execute(SqlTicket._SELECT_BY_ID.format(SqlTicket.TABLE_NAME, id))
        row = cursor.fetchone()
        if row:
            columns_name = [desc[0] for desc in cursor.description]
            cursor.close()
            ticket = self._create_object(columns_name, row)
            return ticket

    def get_join(self, id: int) -> dict:
        cursor = self.connection.cursor()
        cursor.execute(SqlTicket._SELECT_JOIN.format(id))
        row = cursor.fetchone()
        if row:
            columns_name = [desc[0] for desc in cursor.description]
            cursor.close()
            return dict(zip(columns_name, row))

    def update(self, current_ticket: Ticket, new_ticket: Ticket):
        cursor = self.connection.cursor()
        cursor.execute(SqlTicket._UPDATE.format(SqlTicket.TABLE_NAME),
                       (
                           new_ticket.trip_id,
                           new_ticket.origin_id,
                           new_ticket.destination_id,
                           new_ticket.passenger_id,
                           new_ticket.trip_id,
                           new_ticket.route_price,
                           str(current_ticket.id)
                       ))
        self.connection.commit()
        cursor.close()

    def delete(self, id: int):
        cursor = self.connection.cursor()
        cursor.execute(SqlTicket._DELETE.format(SqlTicket.TABLE_NAME, id))
        self.connection.commit()
        cursor.close()

    def _create_object(self, columns_name, data):
        if data:
            data = dict(zip(columns_name, data))
            ticket = Ticket(**data)
            return ticket
        return None

    def rollback(self):
        self.connection.rollback()
