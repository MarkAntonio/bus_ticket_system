import traceback

from flask import Blueprint, make_response, jsonify, request, Response

from bus_ticket_system.app.util import GET, POST, DELETE, PUT, DEFAULT_ERROR
from .business import BusBusiness
from .model import Bus

ROUTE = '/bus'
bp = Blueprint("bus", "__name__", url_prefix=ROUTE)
bus_business = BusBusiness()


@bp.route("/", methods=[POST, GET])
def add():
    try:
        if request.method == POST:
            data = request.form.to_dict()
            has_error, error_msgs = bus_business.validate_fields(data, Bus.FIELDS)
            if not has_error:
                bus = bus_business.save(data)  # retorna o Bus com o id gerado na base
                return make_response(jsonify(bus.to_dict()), 201)

            return make_response(jsonify({'Message': error_msgs}), 400)

        elif request.method == GET:
            bus_type = request.args.get(Bus.TYPE, None)  # obtendo os parâmetros da query
            license = request.args.get(Bus.LICENSE_PLATE, None)

            if bus_type:
                return _search_all_by_type(bus_type)
            if license:
                return _get_by_license(license)
            return _get_all()

    except Exception:
        traceback.print_exc()
        bus_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)


def _get_all():
    buses = bus_business.get()
    if buses:
        result = [bus.to_dict() for bus in buses]
        return make_response(jsonify(result), 200)
    return make_response([])


def _get_by_id(id):
    bus = bus_business.get(id=id)
    if bus:
        return make_response(jsonify(bus.to_dict()), 200)
    return make_response(jsonify({"Message": "Bus id not found"}), 404)


def _get_by_license(license_plate: str):
    bus = bus_business.get(license_plate=license_plate)
    if bus:
        return make_response(jsonify(bus.to_dict()), 200)
    return make_response(jsonify({"Message": f" License plate {license_plate} not found"}), 404)


def _search_all_by_type(type: str):
    buses = bus_business.get(type=type)
    if buses:
        result = [bus.to_dict() for bus in buses]
        return make_response(jsonify(result), 200)
    return make_response({}, 404)


def _update(id):
    current_bus = bus_business.get(id=id)
    data = request.form.to_dict()
    has_error, error_msgs = bus_business.validate_fields(data, Bus.FIELDS)
    if not has_error:
        if current_bus:
            new_bus = Bus(**data, id=id)
            bus_business.update(current_bus, new_bus)
            return make_response(jsonify(new_bus.to_dict()))
        return make_response({"Error": "Bus id not found"}, 404)

    return make_response(jsonify({'Message': error_msgs}), 400)


@bp.route('/<int:id>', methods=[GET, DELETE, PUT])
def delete(id):
    try:
        if request.method == DELETE:
            if bus_business.get(id=id):
                bus_business.delete(id)
                return Response(status=204)
            return make_response({"Message": "Bus id not found"}, 404)
        elif request.method == GET:
            return _get_by_id(id)
        elif request.method == PUT:
            return _update(id)
    except Exception:
        traceback.print_exc()
        bus_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)
