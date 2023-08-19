from . import Route
from flask import Blueprint, make_response, jsonify, request, Response
from bus_ticket_system.app.util import GET, POST, DELETE, PUT, DEFAULT_ERROR
from .business import RouteBusiness
import traceback

ROUTE = '/route'
bp = Blueprint("route", "__name__", url_prefix=ROUTE)
route_business = RouteBusiness()


@bp.route("/", methods=[POST, GET])
def add():
    try:
        if request.method == POST:
            data = request.form.to_dict()
            has_error, error_msgs = route_business.validate_fields(data, Route.FIELDS)
            if not has_error:
                route = route_business.save(data)  # retorna o Route com o id gerado na base
                return make_response(jsonify(route.to_dict()), 201)

            return make_response(jsonify({'Message': error_msgs}), 400)

        elif request.method == GET:
            return _get_all()

    except Exception:
        traceback.print_exc()
        route_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)


def _get_all():
    routes = route_business.get()
    if routes:
        result = [route.to_dict() for route in routes]
        return make_response(jsonify(result), 200)
    return make_response([])


def _get_by_id(id):
    route = route_business.get(id=id)
    if route:
        return make_response(jsonify(route.to_dict()), 200)
    return make_response(jsonify({"Message": "Route id not found"}), 404)


def _update(id):
    current_route = route_business.get(id=id)
    data = request.form.to_dict()
    has_error, error_msgs = route_business.validate_fields(data, Route.FIELDS)
    if not has_error:
        if current_route:
            new_route = Route(**data)
            route_business.update(current_route, new_route)
            return make_response(jsonify(new_route.to_dict()))
        return make_response({"Error": "Route id not found"}, 404)

    return make_response(jsonify({'Message': error_msgs}), 400)


@bp.route('/<int:id>', methods=[GET, DELETE, PUT])
def delete(id):
    try:
        if request.method == DELETE:
            if route_business.get(id=id):
                route_business.delete(id)
                return Response(status=204)
            return make_response({"Message": "Route id not found"}, 404)
        elif request.method == GET:
            return _get_by_id(id)
        elif request.method == PUT:
            return _update(id)

    except Exception:
        traceback.print_exc()
        route_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)
