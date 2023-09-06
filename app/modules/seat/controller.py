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

@bp.route('/', methods=[GET])
def get_all_by_bus():
    try:
        bus_id = request.args.get(Seat.BUS_ID)
        bus = _bus_business.get(id=bus_id)
        if bus:
            seats = seat_business.get(bus_id=bus_id)
            if seats:
                result = [seat.to_dict() for seat in seats]
                return make_response(jsonify(result))
            return make_response([])
        return make_response(jsonify({'msg': f'Seats Bus ID {bus_id} not found'}), 404)

    except Exception:
        traceback.print_exc()
        seat_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)


@bp.route('/<id>', methods=[GET, PUT])
def get_by_id(id: str):
    try:
        seat = seat_business.get(id=id)
        if seat:
            if request.method == GET:
                return make_response(jsonify(seat.to_dict()))

            elif request.method == PUT:
                return _update(seat)

        return make_response(jsonify({'msg': f'Seat id {id} not found'}), 404)

    except Exception:
        traceback.print_exc()
        seat_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)


def _update(current_seat: Seat):
    data = request.form.to_dict()
    data[Seat.ID] = current_seat.id
    data[Seat.BUS_ID] = current_seat.bus_id
    data[Seat.NUMBER] = current_seat.number
    has_error, error_msgs = seat_business.validate_fields(data, Seat.FIELDS)
    if not has_error:
        new_seat = Seat(**data)
        seat_business.update(current_seat, new_seat)
        return make_response(jsonify(new_seat.to_dict()))
    return make_response(jsonify({'Message': error_msgs}), 400)
