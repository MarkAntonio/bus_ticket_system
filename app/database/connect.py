import psycopg2
from bus_ticket_system.app.modules.bus.sql import SqlBus

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
        self._connect.commit()  # Commitando para que o comando seja realizado
        cursor.close()  # fechando a conexão

    def get_instance(self):
        return self._connect


