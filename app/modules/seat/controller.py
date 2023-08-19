from . import Seat
from flask import Blueprint, make_response, jsonify, request, Response
from bus_ticket_system.app.util import GET, POST, DELETE, PUT, DEFAULT_ERROR
from bus_ticket_system.app.modules.bus.controller import bus_business
from .business import SeatBusiness
import traceback

ROUTE = '/seat'
bp = Blueprint("seat", "__name__", url_prefix=ROUTE)
seat_business = SeatBusiness()


def add(data):
    try:
        # como é implementado pelo sistema, não preciso de validação
        seat = seat_business.save(data)  # retorna o Seat com o id gerado na base
        return seat

    except Exception:
        traceback.print_exc()
        seat_business.reconnect()

@bp.route('/<int:bus_id>', methods=[GET])
def get_all_by_bus(bus_id):
    try:
        seats = seat_business.get(bus_id=bus_id)
        if seats:
            result = [seat.to_dict() for seat in seats]
            return make_response(jsonify(result))
        return make_response([])
    except Exception:
        traceback.print_exc()
        seat_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)


def get_by_number(number, bus_id):
    try:
        seat = seat_business.get(number=number, bus_id=bus_id)
        if seat:
            return seat
    except Exception:
        traceback.print_exc()
        seat_business.reconnect()


@bp.route('/', methods=[PUT])
def update():
    try:
        data = request.form.to_dict()
        current_seat = seat_business.get(number=data.get(Seat.NUMBER), bus_id=data.get(Seat.BUS_ID))
        bus = bus_business.get(id=data.get(Seat.BUS_ID))
        print(data)
        if bus:
            if current_seat:
                has_error, error_msgs = seat_business.validate_fields(data, Seat.FIELDS)
                if not has_error:
                    data[Seat.NUMBER] = current_seat.number
                    new_seat = Seat(**data)
                    seat_business.update(current_seat, new_seat)
                    return make_response(jsonify(new_seat.to_dict()))
                return make_response(jsonify({'Message': error_msgs}), 400)

            return make_response({"Error": "Seat number not found"}, 404)

        msg = f"Bus id {data.get(Seat.BUS_ID)} not found"
        return make_response({"Error": msg}, 404)


    except Exception:
        traceback.print_exc()
        seat_business.reconnect()
    return jsonify(DEFAULT_ERROR)


def delete(bus_id):
    try:
        if seat_business.get(bus_id=bus_id):
            seat_business.delete(bus_id)
            return True

    except Exception:
        traceback.print_exc()
        seat_business.reconnect()
