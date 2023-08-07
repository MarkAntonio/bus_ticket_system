from . import Bus
from flask import Blueprint, make_response, jsonify, request, Response
from bus_ticket_system.app.util import to_dict, GET, POST, DELETE, PUT
from .bussiness import BusBussiness
import traceback

ROUTE = '/bus'
bp = Blueprint("bus", "__name__", url_prefix=ROUTE)
bus_bussiness = BusBussiness()
DEFAULT_ERROR = {'Message': 'Ocorreu um erro. Tente novamente ou fale com o suporte.'}


@bp.route("/", methods=[POST, GET])
def add():
    try:
        if request.method == POST:
            data = request.form.to_dict()
            has_error, error_msgs = bus_bussiness.validate_fields(data, Bus.FIELDS)
            if not has_error:
                bus = bus_bussiness.save(data)  # retorna o Bus com o id gerado na base
                return make_response(jsonify(to_dict(bus)), 201)

            return make_response(jsonify({'Message': error_msgs}), 400)

        elif request.method == GET:
            bus_type = request.form.get(Bus.TYPE, None)
            license = request.form.get(Bus.LICENSE_PLATE, None)

            if bus_type:
                return _search_all_by_type(bus_type)
            if license:
                return _get_by_license(license)
            return _get_all()

    except Exception:
        traceback.print_exc()
        bus_bussiness.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)


def _get_all():
    buses = bus_bussiness.get()
    if buses:
        result = [to_dict(bus) for bus in buses]
        return make_response(jsonify(result), 200)
    return make_response([])


def _get_by_id(id):
    bus = bus_bussiness.get(id=id)
    if bus:
        return make_response(jsonify(to_dict(bus)), 200)
    return make_response(jsonify({"Message": "Bus id not found"}), 404)


def _get_by_license(license_plate: str):
    bus = bus_bussiness.get(license_plate=license_plate)
    if bus:
        return make_response(jsonify(to_dict(bus)), 200)
    return make_response(jsonify({"Message": f" License plate {license_plate} not found"}), 404)


def _search_all_by_type(type: str):
    buses = bus_bussiness.get(type=type)
    if buses:
        result = [to_dict(bus) for bus in buses]
        return make_response(jsonify(result), 200)
    return make_response({}, 404)


def _update(id):
    current_bus = bus_bussiness.get(id=id)
    data = request.form.to_dict()
    has_error, error_msgs = bus_bussiness.validate_fields(data, Bus.FIELDS)
    if not has_error:
        new_bus = Bus(**data, id=id)
        if current_bus:
            bus_bussiness.update(current_bus, new_bus)
            return make_response(jsonify(to_dict(new_bus)))
        return make_response({"Error": "Bus id not found"}, 404)

    return make_response(jsonify({'Message': error_msgs}), 400)


@bp.route('/<int:id>', methods=[GET, DELETE, PUT])
def delete(id):
    try:
        if request.method == DELETE:
            if bus_bussiness.get(id=id):
                bus_bussiness.delete(id)
                return Response(status=204)
            return make_response({"Message": "Bus id not found"}, 404)
        elif request.method == GET:
            return _get_by_id(id)
        elif request.method == PUT:
            return _update(id)
    except Exception:
        traceback.print_exc()
        bus_bussiness.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)
