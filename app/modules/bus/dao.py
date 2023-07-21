import psycopg2
import traceback
from bus_ticket_system.app.database import ConnectDataBase
from .model import Bus
from .sql import SqlBus
from psycopg2.errors import CheckViolation, UniqueViolation

class DaoBus:

    def __init__(self):
        self.connection = ConnectDataBase().get_instance()

    def save(self, bus: Bus):
        if bus.id is None:
            cursor = self.connection.cursor()
            try:
                cursor.execute(SqlBus._INSERT,
                               (bus.license_plate,
                                bus.type,
                                bus.amount_seats)
                               )
                self.connection.commit()
                id = cursor.fetchone()[0]
                bus.id = id

            except UniqueViolation as unique_exc:
                self._exception_handling(unique_exc)

            except CheckViolation as check:
                self._exception_handling(check)

            finally:
                cursor.close()

            return bus

    def _exception_handling(self, exception: BaseException):
        self.connection.rollback()  # Roll back all changes done to database due to the error/exception
        traceback.print_exception(exception)
        raise exception

    def get_all(self):
        buses = []
        cursor = self.connection.cursor()
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
        cursor = self.connection.cursor()
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
        cursor = self.connection.cursor()
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
        cursor = self.connection.cursor()
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
        cursor = self.connection.cursor()
        try:
            cursor.execute(SqlBus._UPDATE.format(SqlBus._TABLE_NAME), (
                new_bus.license_plate,
                new_bus.type,
                new_bus.amount_seats,
                str(current_bus.id)))
            self.connection.commit()

        except UniqueViolation as unique_exc:
            self._exception_handling(unique_exc)
        except CheckViolation as check:
            self._exception_handling(check)

        cursor.close()

    def delete(self, id: int):
        cursor = self.connection.cursor()
        cursor.execute(SqlBus._DELETE.format(SqlBus._TABLE_NAME, id))
        self.connection.commit()
        cursor.close()
