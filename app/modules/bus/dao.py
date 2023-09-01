from app.util import BaseDAO
from .model import Bus
from .sql import SqlBus


class BusDao(BaseDAO):

    def save(self, bus: Bus):
        cursor = self._save(SqlBus._INSERT,
                            (bus.license_plate,
                             bus.type,
                             bus.amount_seats)
                            )
        bus.id = cursor.fetchone()[0]
        cursor.close()
        return bus

    def get_all(self):
        return self._get_all(SqlBus._SELECT_ALL, Bus)

    def get_by_id(self, id: int):
        return self._get_by(SqlBus._SELECT_BY_ID.format(SqlBus.TABLE_NAME, id), Bus)

    def get_by_license(self, license: str):
        return self._get_by(SqlBus._SELECT_BY_LICENSE.format(SqlBus.TABLE_NAME, license), Bus)

    def get_all_by_type(self, type: str):
        return self._get_all(SqlBus._SEARCH_TYPES.format(SqlBus.TABLE_NAME, type), Bus)

    def update(self, current_bus: Bus, new_bus: Bus):
        self._update(SqlBus._UPDATE.format(SqlBus.TABLE_NAME),
                     (new_bus.license_plate, new_bus.type, new_bus.amount_seats, str(current_bus.id)))

    def delete(self, id: int):
        self._delete(SqlBus._DELETE.format(SqlBus.TABLE_NAME, id))
