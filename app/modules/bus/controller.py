from .dao import DaoBus
from . import Bus
from flask import Blueprint, make_response, jsonify, request, Response

dao = DaoBus()
bp = Blueprint("bus", "__name__")

POST = "POST"
GET = "GET"
DELETE = "DELETE"
PUT = "PUT"


@bp.route("/", methods=[POST, GET])
def add():
    if request.method == POST:
        bus = Bus(request.form["license_plate"], request.form["type"], request.form["amount_seats"])
        bus = dao.save(bus)  # retorna o Bus com o id gerado na base
        return make_response(jsonify(bus.to_dict()), 201)

    elif request.method == GET:
        bus_type = request.form.get('type', None)
        if bus_type:
            return _search_all_by_type(bus_type)
        return _get_all()


def _get_all():
    buses = dao.get_all()
    result = [bus.to_dict() for bus in buses]
    return make_response(jsonify(result), 200)


def _get_by_id(id):
    bus = dao.get_by_id(id)
    return make_response(jsonify(bus.to_dict()), 200)

@bp.route('/<license_plate>')
def get_by_license(license_plate: str):
    bus = dao.get_by_license(license_plate)
    return make_response(jsonify(bus.to_dict()), 200)


def _search_all_by_type(type:str):
    buses = dao.get_all_by_type(type)
    result = [bus.to_dict() for bus in buses]
    return make_response(jsonify(result), 200)


def _update(id):
    current_bus = dao.get_by_id(id)
    new_bus = Bus(request.form['license_plate'], request.form['type'], request.form['amount_seats'], id)
    dao.update(current_bus, new_bus)
    return make_response(jsonify(new_bus.to_dict()), 200)


@bp.route('/<int:id>', methods=[GET, DELETE, PUT])
def delete(id):
    if request.method == DELETE:
        dao.delete(id)
        return Response(status=204)
    elif request.method == GET:
        return _get_by_id(id)
    elif request.method == PUT:
        return _update(id)
