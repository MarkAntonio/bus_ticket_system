from .model import Route
from .sql import SqlRoute
from app.util import BaseDAO


class RouteDao(BaseDAO):

    def save(self, route: Route):
        cursor = self._save(SqlRoute._INSERT,
                            (
                                route.city,
                                Route.time_to_str(route.time),
                                route.price,
                                route.line_id
                            ))
        route.id = cursor.fetchone()[0]
        cursor.close()
        return route

    def get_all(self):
        return self._get_all(SqlRoute._SELECT_ALL, Route)

    def get_all_by_line(self, line_id: int):
        return self._get_all(SqlRoute._SELECT_ALL_BY_LINE.format(SqlRoute.TABLE_NAME, line_id), Route)

    def get_by_id(self, id: int):
        return self._get_by(SqlRoute._SELECT_BY_ID.format(SqlRoute.TABLE_NAME, id), Route)

    def update(self, current_route: Route, new_route: Route):
        self._update(SqlRoute._UPDATE.format(SqlRoute.TABLE_NAME),
                       (
                           new_route.city,
                           Route.time_to_str(new_route.time),
                           new_route.price,
                           current_route.line_id,
                           str(current_route.id)
                       ))

    def delete(self, id: int):
        self._delete(SqlRoute._DELETE.format(SqlRoute.TABLE_NAME, id))
