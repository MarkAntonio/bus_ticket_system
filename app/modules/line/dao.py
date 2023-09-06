from app.database import ConnectDataBase
from .model import Line
from .sql import SqlLine
from app.util import BaseDAO


class LineDao(BaseDAO):

    def save(self, line: Line):
        cursor = self._save(SqlLine._INSERT,
                            (line.origin,
                             line.destination,
                             Line.time_to_str(line.departure_time),
                             Line.time_to_str(line.arrival_time),
                             line.total_price))
        line.id = cursor.fetchone()[0]
        cursor.close()
        return line

    def get_all(self):
        return self._get_all(SqlLine._SELECT_ALL, Line)

    def get_by_id(self, id: int):
        return self._get_by(SqlLine._SELECT_BY_ID.format(SqlLine.TABLE_NAME, id), Line)

    def update(self, current_line: Line, new_line: Line):
        self._update(SqlLine._UPDATE.format(SqlLine.TABLE_NAME),
                     (
                         new_line.origin,
                         new_line.destination,
                         Line.time_to_str(new_line.departure_time),
                         Line.time_to_str(new_line.arrival_time),
                         new_line.total_price,
                         str(current_line.id)
                     ))

    def delete(self, id: int):
        self._delete(SqlLine._DELETE.format(SqlLine.TABLE_NAME, id))
