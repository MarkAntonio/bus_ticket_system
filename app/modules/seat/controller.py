from . import Seat
from flask import Blueprint, make_response, jsonify, request, Response
from bus_ticket_system.app.util import GET, POST, DELETE, PUT, DEFAULT_ERROR
from .business import SeatBusiness
import traceback

ROUTE = '/seat'
bp = Blueprint("seat", "__name__", url_prefix=ROUTE)
seat_business = SeatBusiness()


@bp.route("/", methods=[POST, GET])
def add():
    try:
        if request.method == POST:
            data = request.form.to_dict()
            has_error, error_msgs = seat_business.validate_fields(data, Seat.FIELDS)
            if not has_error:
                seat = seat_business.save(data)  # retorna o Seat com o id gerado na base
                return make_response(jsonify(seat.to_dict()), 201)

            return make_response(jsonify({'Message': error_msgs}), 400)

        elif request.method == GET:
            return _get_all()

    except Exception:
        traceback.print_exc()
        seat_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)


def _get_all():
    seats = seat_business.get()
    if seats:
        result = [seat.to_dict() for seat in seats]
        return make_response(jsonify(result), 200)
    return make_response([])


def _get_by_id(id):
    seat = seat_business.get(id=id)
    if seat:
        return make_response(jsonify(seat.to_dict()), 200)
    return make_response(jsonify({"Message": "Seat id not found"}), 404)


def _update(id):
    current_seat = seat_business.get(id=id)
    data = request.form.to_dict()
    has_error, error_msgs = seat_business.validate_fields(data, Seat.FIELDS)
    if not has_error:
        if current_seat:
            new_seat = Seat(**data)
            seat_business.update(current_seat, new_seat)
            return make_response(jsonify(new_seat.to_dict()))
        return make_response({"Error": "Seat id not found"}, 404)

    return make_response(jsonify({'Message': error_msgs}), 400)


@bp.route('/<int:id>', methods=[GET, DELETE, PUT])
def delete(id):
    try:
        if request.method == DELETE:
            if seat_business.get(id=id):
                seat_business.delete(id)
                return Response(status=204)
            return make_response({"Message": "Seat id not found"}, 404)
        elif request.method == GET:
            return _get_by_id(id)
        elif request.method == PUT:
            return _update(id)

    except Exception:
        traceback.print_exc()
        seat_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)
