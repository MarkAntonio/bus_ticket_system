from datetime import datetime


class Trip:
    ID = 'id'
    DATE = 'date'
    LINE_ID = 'line_id'
    BUS_ID = 'bus_id'
    FIELDS = [DATE, LINE_ID, BUS_ID]

    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, date: datetime, line_id, bus_id, id=None):
        self.id = id
        self.date = date
        self.line_id = line_id
        self.bus_id = bus_id

    @classmethod
    def str_to_datetime(cls, trip_date: str):
        return datetime.strptime(trip_date, cls.DATE_FORMAT)

    @classmethod
    def datetime_to_str(cls, trip_date: datetime):
        return trip_date.strftime(cls.DATE_FORMAT)

    def to_dict(self):
        return {
            self.ID: self.id,
            self.DATE: self.datetime_to_str(self.date),
            self.LINE_ID: self.line_id,
            self.BUS_ID: self.bus_id
        }
