from app.database import ConnectDataBase
from .model import Route
from .sql import SqlRoute


class RouteDao:

    def __init__(self):
        self.connection = ConnectDataBase().get_instance()

    def save(self, route: Route):
        cursor = self.connection.cursor()
        cursor.execute(SqlRoute._INSERT,
                       (route.city,
                        route.time,
                        route.price,
                        route.line_id)
                       )
        self.connection.commit()
        route.id = cursor.fetchone()[0]
        cursor.close()
        return route

    def get_all(self, line_id: int):
        routes = []
        cursor = self.connection.cursor()
        cursor.execute(SqlRoute._SELECT_ALL.format(SqlRoute.TABLE_NAME, line_id))
        result = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]

        for row in result:
            routes.append(self._create_object(columns_name, row))

        cursor.close()
        if routes:
            return routes

    def get_by_id(self, id: int, line_id: int):
        cursor = self.connection.cursor()
        cursor.execute(SqlRoute._SELECT_BY_ID.format(SqlRoute.TABLE_NAME, id, line_id))
        row = cursor.fetchone()
        if row:
            columns_name = [desc[0] for desc in cursor.description]
            cursor.close()
            route = self._create_object(columns_name, row)
            return route

    def update(self, current_route: Route, new_route: Route):
        cursor = self.connection.cursor()
        cursor.execute(SqlRoute._UPDATE.format(SqlRoute.TABLE_NAME),
                       (
                        new_route.city,
                        Route.time_to_str(new_route.time),
                        new_route.price,
                        str(current_route.id),
                        str(current_route.line_id)
                        ))
        self.connection.commit()
        cursor.close()

    def delete(self, id: int, line_id: int):
        cursor = self.connection.cursor()
        cursor.execute(SqlRoute._DELETE.format(SqlRoute.TABLE_NAME, id, line_id))
        self.connection.commit()
        cursor.close()

    def _create_object(self, columns_name, data):
        if data:
            data = dict(zip(columns_name, data))
            route = Route(**data)
            return route
        return None

    def rollback(self):
        self.connection.rollback()
