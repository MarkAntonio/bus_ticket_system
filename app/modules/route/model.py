from datetime import datetime, time


class Route:

    ID = 'id'
    CITY = 'city'
    TIME = 'time'
    # preço da cidade de embarque até a cidade final.
    # A cidade inicial tem o preço total que está na Line. Aqui teremos as cidades que intermedeiam a linha do ônibus.
    PRICE = 'price'
    LINE_ID = 'line_id'
    FIELDS = [CITY, TIME, PRICE, LINE_ID]

    _HOUR_FORMAT = '%H:%M'

    def __init__(self, city: str, time: str, price:str, line_id:str, id=None):
        self.id = id
        self.city = city
        self.time = time
        self.price = price
        self.line_id = line_id

    @classmethod
    def str_to_time(cls, value: str) -> time:
        return datetime.strptime(value, cls._HOUR_FORMAT).time()

    @classmethod
    def time_to_str(cls, value: time) -> str:
        return value.strftime(cls._HOUR_FORMAT)

    def to_dict(self):
        return {
            self.ID: self.id,
            self.CITY: self.city,
            self.TIME: self.time_to_str(self.time),
            self.PRICE: self.price,
            self.LINE_ID: self.line_id
        }
