from bus_ticket_system.app.database import ConnectDataBase
from .model import Bus
from .sql import SqlBus


class BusDao:

    def __init__(self):
        self.connection = ConnectDataBase().get_instance()

    def save(self, bus: Bus):
        cursor = self.connection.cursor()
        cursor.execute(SqlBus._INSERT,
                       (bus.license_plate,
                        bus.type,
                        bus.amount_seats)
                       )
        self.connection.commit()
        bus.id = cursor.fetchone()[0]
        cursor.close()
        return bus

    def get_all(self):
        buses = []
        cursor = self.connection.cursor()
        cursor.execute(SqlBus._SELECT_ALL)
        result = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]

        for row in result:
            buses.append(self._create_object(columns_name, row))

        cursor.close()
        if buses:
            return buses

    def get_by_id(self, id: int):
        cursor = self.connection.cursor()
        cursor.execute(SqlBus._SELECT_BY_ID.format(SqlBus.TABLE_NAME, id))
        row = cursor.fetchone()
        if row:
            columns_name = [desc[0] for desc in cursor.description]
            cursor.close()
            bus = self._create_object(columns_name, row)
            return bus

    def get_by_license(self, license: str):
        cursor = self.connection.cursor()
        cursor.execute(SqlBus._SELECT_BY_LICENSE.format(SqlBus.TABLE_NAME, license))
        row = cursor.fetchone()
        if not row:
            return None
        columns_name = [desc[0] for desc in cursor.description]
        cursor.close()
        bus = self._create_object(columns_name, row)
        return bus

    def get_all_by_type(self, type: str):
        buses = []
        cursor = self.connection.cursor()
        cursor.execute(SqlBus._SEARCH_TYPES.format(SqlBus.TABLE_NAME, type))
        result = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        cursor.close()

        for row in result:
            buses.append(self._create_object(columns_name, row))

        if buses:
            return buses

    def update(self, current_bus: Bus, new_bus: Bus):
        cursor = self.connection.cursor()
        cursor.execute(SqlBus._UPDATE.format(SqlBus.TABLE_NAME), (
            new_bus.license_plate,
            new_bus.type,
            new_bus.amount_seats,
            str(current_bus.id)))
        self.connection.commit()
        cursor.close()

    def delete(self, id: int):
        cursor = self.connection.cursor()
        cursor.execute(SqlBus._DELETE.format(SqlBus.TABLE_NAME, id))
        self.connection.commit()
        cursor.close()

    def _create_object(self, columns_name, data):
        if data:
            data = dict(zip(columns_name, data))
            bus = Bus(**data)
            return bus
        return None

    def rollback(self):
        self.connection.rollback()
