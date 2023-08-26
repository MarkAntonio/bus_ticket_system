from . import Seat
from flask import Blueprint, make_response, jsonify, request
from app.util import GET, PUT, DEFAULT_ERROR
from app.modules.bus.business import BusBusiness
from .business import SeatBusiness
from app.modules.bus import Bus
import traceback

ROUTE = '/seat'
bp = Blueprint("seat", "__name__", url_prefix=ROUTE)
seat_business = SeatBusiness()
_bus_business = BusBusiness()

# A rota ADD deve ser acessada somente pelo sistema diretamente no Business do Seat
# def add(data):
#     try:
#         # como é implementado pelo sistema, não preciso de validação
#         number = data[Seat.NUMBER]
#         number = number if int(number) > 9 else '0' + number
#         # o id é gerado pelo sistema e não pelo banco de dados
#         # o id depende da placa do ônibus e do número do assento
#         # ex: Seat id= KHA9H12-03
#         id = data[Seat.BUS_ID] + '-' + number
#         data[Seat.ID] = id
#         seat = seat_business.save(data)  # retorna o Seat com o id gerado na base
#         return seat
#
    # except Exception:
    #     traceback.print_exc()
    #     seat_business.reconnect()


@bp.route('/<int:bus_id>', methods=[GET])
def get(bus_id):
    try:
        bus = _bus_business.get(id=bus_id)
        if bus:
            seat_id = request.form.get(Seat.ID)
            if seat_id:
                seat = seat_business.get(id=seat_id)
                if seat:
                    return _get_by_id(seat_id)
            return _get_all_by_bus(bus_id)
        return make_response(jsonify({'msg': f'Seats Bus ID {bus_id} not found'}), 404)
    except Exception:
        traceback.print_exc()
        seat_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)


def _get_all_by_bus(bus_id):
    seats = seat_business.get(bus_id=bus_id)

    if seats:
        result = [seat.to_dict() for seat in seats]
        return make_response(jsonify(result))
    return make_response([])


def _get_by_id(id):
    seat = seat_business.get(id=id)
    if seat:
        return make_response(jsonify(seat.to_dict()))
    return make_response(jsonify({'msg': f'Seat id {id} not found'}), 404)


@bp.route('/', methods=[PUT])
def update():
    try:
        data = request.form.to_dict()
        bus = _bus_business.get(id=data.get(Seat.BUS_ID))
        if bus:
            current_seat = seat_business.get(id=data.get(Seat.ID), bus_id=data.get(Seat.BUS_ID))
            if current_seat:
                has_error, error_msgs = seat_business.validate_fields(data, Seat.FIELDS)
                if not has_error:
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


# A rota DELETE somente deve ser acessada pelo sistema
def delete(bus_id):
    try:
        if seat_business.get(bus_id=bus_id):
            seat_business.delete(bus_id)
            return True

    except Exception:
        traceback.print_exc()
        seat_business.reconnect()
