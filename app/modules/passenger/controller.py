from . import Passenger
from flask import Blueprint, make_response, jsonify, request, Response
from app.util import GET, POST, DELETE, PUT, DEFAULT_ERROR
from .business import PassengerBusiness
import traceback

ROUTE = '/passenger'
bp = Blueprint("passenger", "__name__", url_prefix=ROUTE)
passenger_business = PassengerBusiness()


@bp.route("/", methods=[POST, GET])
def add():
    try:
        if request.method == POST:
            data = request.form.to_dict()
            has_error, error_msgs = passenger_business.validate_fields(data, Passenger.FIELDS)
            if not has_error:
                passenger = passenger_business.save(data)  # retorna o Passenger com o id gerado na base
                return make_response(jsonify(passenger.to_dict()), 201)

            return make_response(jsonify({'Message': error_msgs}), 400)

        elif request.method == GET:
            return _get_all()

    except Exception:
        traceback.print_exc()
        passenger_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)


def _get_all():
    passengers = passenger_business.get()
    if passengers:
        result = [passenger.to_dict() for passenger in passengers]
        return make_response(jsonify(result), 200)
    return make_response([])


def _get_by_id(id):
    passenger = passenger_business.get(id=id)
    if passenger:
        return make_response(jsonify(passenger.to_dict()), 200)
    return make_response(jsonify({"Message": "Passenger id not found"}), 404)


def _update(id):
    current_passenger = passenger_business.get(id=id)
    data = request.form.to_dict()
    has_error, error_msgs = passenger_business.validate_fields(data, Passenger.FIELDS)
    if not has_error:
        if current_passenger:
            new_passenger = Passenger(**data)
            passenger_business.update(current_passenger, new_passenger)
            return make_response(jsonify(new_passenger.to_dict()))
        return make_response({"Error": "Passenger id not found"}, 404)

    return make_response(jsonify({'Message': error_msgs}), 400)


@bp.route('/<int:id>', methods=[GET, DELETE, PUT])
def delete(id):
    try:
        if request.method == DELETE:
            # verificando se o passageiro existe
            if passenger_business.get(id=id):
                passenger_business.delete(id)
                return Response(status=204)
            return make_response({"Message": "Passenger id not found"}, 404)
        elif request.method == GET:
            return _get_by_id(id)
        elif request.method == PUT:
            return _update(id)

    except Exception:
        traceback.print_exc()
        passenger_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)
