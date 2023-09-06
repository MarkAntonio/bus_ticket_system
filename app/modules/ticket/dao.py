from app.util import BaseDAO
from .model import Ticket
from .sql import SqlTicket


class TicketDao(BaseDAO):

    def save(self, ticket: Ticket):
        cursor = self._save(SqlTicket._INSERT,
                            (
                                ticket.trip_id,
                                ticket.origin_id,
                                ticket.destination_id,
                                ticket.passenger_id,
                                ticket.seat_id,
                                ticket.route_price
                            ))
        ticket.id = cursor.fetchone()[0]
        cursor.close()
        return ticket

    def get_all(self):
        return self._get_all(SqlTicket._SELECT_ALL, Ticket)

    def get_by_id(self, id: int):
        return self._get_by(SqlTicket._SELECT_BY_ID.format(SqlTicket.TABLE_NAME, id), Ticket)

    def get_join(self, id: int) -> dict:
        cursor = self.connection.cursor()
        cursor.execute(SqlTicket._SELECT_JOIN.format(id))
        row = cursor.fetchone()
        cursor.close()
        if row:
            columns_name = [desc[0] for desc in cursor.description]
            return dict(zip(columns_name, row))

    def update(self, current_ticket: Ticket, new_ticket: Ticket):
        self._update(SqlTicket._UPDATE.format(SqlTicket.TABLE_NAME),
                     (
                         new_ticket.trip_id,
                         new_ticket.origin_id,
                         new_ticket.destination_id,
                         new_ticket.passenger_id,
                         new_ticket.trip_id,
                         new_ticket.route_price,
                         str(current_ticket.id)
                     ))

    def delete(self, id: int):
        self._delete(SqlTicket._DELETE.format(SqlTicket.TABLE_NAME, id))
