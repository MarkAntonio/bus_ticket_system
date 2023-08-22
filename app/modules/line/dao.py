from app.database import ConnectDataBase
from .model import Line
from .sql import SqlLine


class LineDao:

    def __init__(self):
        self.connection = ConnectDataBase().get_instance()

    def save(self, line: Line):
        cursor = self.connection.cursor()
        cursor.execute(SqlLine._INSERT,
                       (line.origin,
                        line.destination,
                        Line.time_to_str(line.departure_time),
                        Line.time_to_str(line.arrival_time),
                        line.total_price)
                       )
        self.connection.commit()
        line.id = cursor.fetchone()[0]
        cursor.close()
        return line

    def get_all(self):
        lines = []
        cursor = self.connection.cursor()
        cursor.execute(SqlLine._SELECT_ALL)
        result = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]

        for row in result:
            lines.append(self._create_object(columns_name, row))

        cursor.close()
        if lines:
            return lines

    def get_by_id(self, id: int):
        cursor = self.connection.cursor()
        cursor.execute(SqlLine._SELECT_BY_ID.format(SqlLine.TABLE_NAME, id))
        row = cursor.fetchone()
        if row:
            columns_name = [desc[0] for desc in cursor.description]
            cursor.close()
            line = self._create_object(columns_name, row)
            return line

    def update(self, current_line: Line, new_line: Line):
        cursor = self.connection.cursor()
        cursor.execute(SqlLine._UPDATE.format(SqlLine.TABLE_NAME), (
            new_line.origin,
            new_line.destination,
            Line.time_to_str(new_line.departure_time),
            Line.time_to_str(new_line.arrival_time),
            new_line.total_price,
            str(current_line.id)))
        self.connection.commit()
        cursor.close()


    def delete(self, id: int):
        cursor = self.connection.cursor()
        cursor.execute(SqlLine._DELETE.format(SqlLine.TABLE_NAME, id))
        self.connection.commit()
        cursor.close()

    def _create_object(self, columns_name, data):
        if data:
            data = dict(zip(columns_name, data))
            line = Line(**data)
            return line
        return None

    def rollback(self):
        self.connection.rollback()
