import re

from app.util import BaseValidate
from .dao import PassengerDao
from .model import Passenger


class PassengerBusiness(BaseValidate):
    # Expressão regular para identificar padrão de número de telefone
    _PHONE_REGEX = re.compile(r'\(\d{2}\)9\d{4}-\d{4}$')

    def __init__(self):
        self.__passenger_dao = PassengerDao()

    def save(self, data):
        passenger = self.__passenger_dao.save(Passenger(**data))  # atribui o id para eu retornar para a API
        return passenger

    def get(self, **kwargs):
        if not kwargs:
            return self.__passenger_dao.get_all()
        elif kwargs.get(Passenger.ID):
            return self.__passenger_dao.get_by_id(kwargs[Passenger.ID])
        raise Exception('Field not exists')  # caso o programador coloque um campo que não existe ou está incorreto

    def update(self, current_passenger, new_passenger):
        self.__passenger_dao.update(current_passenger, new_passenger)

    def delete(self, id):
        self.__passenger_dao.delete(id)

    def reconnect(self):
        self.__passenger_dao.rollback()

    def _validate_phone(self, phone):
        if not self._PHONE_REGEX.match(phone):
            return "The phone number is incorrect. Try a number format such as (xx)9xxxx-xxxx where x = digit."

