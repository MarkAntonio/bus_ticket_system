from .model import Route
from .sql import SqlRoute
from app.util import BaseDAO

class RouteDao(BaseDAO):

    def save(self, route: Route):
        cursor = self.connection.cursor()
        cursor.execute(SqlRoute._INSERT,
                       (
                           route.city,
                           Route.time_to_str(route.time),
                           route.price,
                           route.line_id
                       ))
        self.connection.commit()
        route.id = cursor.fetchone()[0]
        cursor.close()
        return route

    def get_all(self):
        routes = []
        cursor = self.connection.cursor()
        cursor.execute(SqlRoute._SELECT_ALL)
        result = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]

        for row in result:
            routes.append(self._create_object(columns_name, row, Route))

        cursor.close()
        if routes:
            return routes

    def get_all_by_line(self, line_id: int):
        routes = []
        cursor = self.connection.cursor()
        cursor.execute(SqlRoute._SELECT_ALL_BY_LINE.format(SqlRoute.TABLE_NAME, line_id))
        result = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]

        for row in result:
            routes.append(self._create_object(columns_name, row, Route))

        cursor.close()
        if routes:
            return routes

    def get_by_id(self, id: int):
        cursor = self.connection.cursor()
        cursor.execute(SqlRoute._SELECT_BY_ID.format(SqlRoute.TABLE_NAME, id))
        row = cursor.fetchone()
        if row:
            columns_name = [desc[0] for desc in cursor.description]
            cursor.close()
            route = self._create_object(columns_name, row, Route)
            return route

    def update(self, current_route: Route, new_route: Route):
        cursor = self.connection.cursor()
        cursor.execute(SqlRoute._UPDATE.format(SqlRoute.TABLE_NAME),
                       (
                           new_route.city,
                           Route.time_to_str(new_route.time),
                           new_route.price,
                           current_route.line_id,
                           str(current_route.id)
                       ))
        self.connection.commit()
        cursor.close()

    def set_line_id(self, id, line_id):
        cursor = self.connection.cursor()
        cursor.execute(SqlRoute._UPDATE.format(SqlRoute.TABLE_NAME), (
            str(line_id),
            str(id)
        ))
        self.connection.commit()
        cursor.close()

    def delete(self, id: int):
        cursor = self.connection.cursor()
        cursor.execute(SqlRoute._DELETE.format(SqlRoute.TABLE_NAME, id))
        self.connection.commit()
        cursor.close()
