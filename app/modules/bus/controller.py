import psycopg2.errors

from .dao import DaoBus
from . import Bus
from flask import Blueprint, make_response, jsonify, request, Response
from bus_ticket_system.app import util
import re  # Regular Expressions

dao = DaoBus()
bp = Blueprint("bus", "__name__")

POST = "POST"
GET = "GET"
DELETE = "DELETE"
PUT = "PUT"

_LICENSE_REGEX = re.compile(r'^[A-Z]{3}\d[A-Z]\d{2}$')


@bp.route("/", methods=[POST, GET])
def add():
    if request.method == POST:
        data, authenticated = util.validate_fields(request, Bus)
        if authenticated:
            bus = Bus(**data)
            try:
                bus = dao.save(bus)  # retorna o Bus com o id gerado na base
                return make_response(jsonify(util.to_dict(bus)), 201)
            except psycopg2.errors.UniqueViolation:
                return make_response(
                    jsonify({"Error": 'The key license_plate is UNIQUE and the value '
                                      f'[{bus.license_plate}] is already registered'}), 409)
            except psycopg2.errors.CheckViolation:
                return make_response(
                    jsonify({"Error": "The license_plate format incorrect. "
                                      "The format must have the following sequence: AAA9A99"}), 400)

        return make_response(jsonify(data), 400)

    elif request.method == GET:
        bus_type = request.form.get('type', None)
        license = request.form.get('license_plate', None)
        if bus_type:
            return _search_all_by_type(bus_type)
        if license:
            return _get_by_license(license)
        return _get_all()


def _get_all():
    buses = dao.get_all()
    if buses:
        result = [util.to_dict(bus) for bus in buses]
        return make_response(jsonify(result), 200)
    return make_response({})


def _get_by_id(id):
    bus = dao.get_by_id(id)
    if bus:
        return make_response(jsonify(util.to_dict(bus)), 200)
    return make_response(jsonify({"Error": "Bus id not found"}), 404)



def _get_by_license(license_plate: str):
    bus = dao.get_by_license(license_plate)
    if bus:
        return make_response(jsonify(util.to_dict(bus)), 200)
    return make_response(jsonify({"Error": f" License plate {license_plate} not found"}), 404)


def _search_all_by_type(type: str):
    buses = dao.get_all_by_type(type)
    if buses:
        result = [util.to_dict(bus) for bus in buses]
        return make_response(jsonify(result), 200)
    return make_response({}, 404)


def _update(id):
    current_bus = dao.get_by_id(id)
    license = request.form['license_plate'].upper()  # colocando todas as letras em maiúsculas
    new_bus = Bus(license, request.form['type'], request.form['amount_seats'], id)
    if current_bus:
        try:
            dao.update(current_bus, new_bus)
            return make_response(jsonify(util.to_dict(new_bus)))
        except psycopg2.errors.UniqueViolation:
            return make_response(
                jsonify({"Error": 'The key license_plate is UNIQUE and the value '
                                  f'[{new_bus.license_plate}] is already registered'}), 409)
        except psycopg2.errors.CheckViolation:
            errors = bus_check_violations(license)
            return make_response(
                jsonify({"Error": errors}), 400)
    return make_response({"Error": "Bus id not found"}, 404)

def bus_check_violations(license):
    errors = []
    available_types = ('Convencional', 'Executivo', 'Leito', 'Leito Cama')
    if not _LICENSE_REGEX.match(license):
        errors.append("The license_plate format incorrect. The format must have the following sequence: AAA9A99")

    if not request.form['type'] in available_types:
        errors.append(f"Type's incorrect. Try to put some of these: {available_types}")
    return errors

@bp.route('/<int:id>', methods=[GET, DELETE, PUT])
def delete(id):
    if request.method == DELETE:
        if dao.get_by_id(id):
            dao.delete(id)
            return Response(status=204)
        return make_response({"Error": "Bus id not found"}, 404)
    elif request.method == GET:
        return _get_by_id(id)
    elif request.method == PUT:
        return _update(id)
