import psycopg2
from app.modules.bus import SqlBus
from app.modules.line import SqlLine
from app.modules.passenger import SqlPassenger
from app.modules.seat import SqlSeat
from app.modules.route import SqlRoute
from app.modules.trip import SqlTrip
from app.modules.ticket import SqlTicket


class ConnectDataBase:

    def __init__(self):
        self._connect = psycopg2.connect(
            host='localhost',
            database='bus_ticket_system',
            user='postgres',
            password='91397114'
        )

    def init_table(self):
        cursor = self._connect.cursor()
        cursor.execute(SqlBus._CREATE_TABLE)  # Inicializar cada uma das tables
        cursor.execute(SqlLine._CREATE_TABLE)
        cursor.execute(SqlPassenger._CREATE_TABLE)
        cursor.execute(SqlSeat._CREATE_TABLE)
        cursor.execute(SqlRoute._CREATE_TABLE)
        cursor.execute(SqlTrip._CREATE_TABLE)
        cursor.execute(SqlTicket._CREATE_TABLE)
        self._connect.commit()  # Commitando para que o comando seja realizado
        cursor.close()  # fechando a conexão

    def get_instance(self):
        return self._connect
