from bus_ticket_system.app.database import ConnectDataBase
from .model import Bus
from .sql import SqlBus


class DaoBus:

    def __init__(self):
        self.database = ConnectDataBase().get_instance()

    def save(self, bus: Bus):
        if bus.id is None:
            cursor = self.database.cursor()
            cursor.execute(SqlBus._INSERT,
                           (bus.license_plate,
                            bus.type,
                            bus.amount_seats)
                           )
            self.database.commit()
            id = cursor.fetchone()[0]
            bus.id = id
            return bus

    def get_all(self):
        buses = []
        cursor = self.database.cursor()
        cursor.execute(SqlBus._SELECT_ALL.format(SqlBus._TABLE_NAME))
        result = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]

        for row in result:
            bus_kwags = dict(zip(columns_name, row))
            bus = Bus(**bus_kwags)
            buses.append(bus)

        cursor.close()
        if buses:
            return buses

    def get_by_id(self, id: int):
        cursor = self.database.cursor()
        cursor.execute(SqlBus._SELECT_BY_ID.format(SqlBus._TABLE_NAME, id))
        row = cursor.fetchone()
        if not row:
            return None
        columns_name = [desc[0] for desc in cursor.description]
        cursor.close()
        kwargs = dict(zip(columns_name, row))
        bus = Bus(**kwargs)
        return bus

    def get_by_license(self, license: str):
        cursor = self.database.cursor()
        cursor.execute(SqlBus._SELECT_BY_LICENSE.format(SqlBus._TABLE_NAME, license))
        row = cursor.fetchone()
        if not row:
            return None
        columns_name = [desc[0] for desc in cursor.description]
        cursor.close()
        kwargs = dict(zip(columns_name, row))
        bus = Bus(**kwargs)
        return bus

    def get_all_by_type(self, type: str):
        buses = []
        cursor = self.database.cursor()
        cursor.execute(SqlBus._SEARCH_TYPES.format(SqlBus._TABLE_NAME, type))
        result = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        cursor.close()

        for row in result:
            bus_kwags = dict(zip(columns_name, row))
            bus = Bus(**bus_kwags)
            buses.append(bus)

        if buses:
            return buses

    def update(self, current_bus: Bus, new_bus: Bus):
        cursor = self.database.cursor()
        cursor.execute(SqlBus._UPDATE.format(SqlBus._TABLE_NAME),(
                       new_bus.license_plate,
                       new_bus.type,
                       new_bus.amount_seats,
                       str(current_bus.id))
                       )
        self.database.commit()
        cursor.close()

    def delete(self, id: int):
        cursor = self.database.cursor()
        cursor.execute(SqlBus._DELETE.format(SqlBus._TABLE_NAME, id))
        self.database.commit()
        cursor.close()

