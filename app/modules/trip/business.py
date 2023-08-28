import re  # Regular Expressions
from datetime import date
from app.util import BaseValidate
from .model import Trip
from .dao import TripDao

from app.modules.seat import Seat


class TripBusiness(BaseValidate):
    _CURRENT_YEAR = date.today().year
    _DATE_REGEX = re.compile(r'^(\d{4})-(?:0\d|1[0-2])-(?:0\d|1\d|2\d|3[01])$')

    def __init__(self):
        self.__trip_dao = TripDao()

    def save(self, data):
        # convertendo a data para o tipo datetime
        data[Trip.DATE] = Trip.str_to_datetime(data[Trip.DATE])
        trip = self.__trip_dao.save(Trip(**data))  # atribui o id para eu retornar para a AP
        return trip

    def get(self, **kwargs):
        if not kwargs:
            return self.__trip_dao.get_all()
        elif kwargs.get(Trip.ID):
            return self.__trip_dao.get_by_id(kwargs[Trip.ID])
        raise Exception('Field not exists')  # caso o programador coloque um campo que não existe ou está incorreto

    def update(self, current_trip: Trip, new_trip: Trip):
        new_trip.date = Trip.str_to_datetime(new_trip.date)
        self.__trip_dao.update(current_trip, new_trip)

    def delete(self, id):
        self.__trip_dao.delete(id)

    def _validate_date(self, date):
        match_date = self._DATE_REGEX.match(date)
        if not match_date:
            return "The date format is incorrect. The format must be YYYY-MM-DD such as 2023-08-23."
        year = match_date.group(1)
        if int(year) < self._CURRENT_YEAR:
            return f"Try put a year >= {self._CURRENT_YEAR}."

    def _validate_bus_id(self, bus_id:str):
        if not bus_id.isnumeric():
            return 'Bus id must be a number.'

    def _validate_line_id(self, line_id:str):
        if not line_id.isnumeric():
            return 'Line id must be a number.'

    def reconnect(self):
        self.__trip_dao.rollback()
