import traceback

from flask import Blueprint, make_response, jsonify, request, Response

from app.modules.line.controller import line_business
from app.util import GET, POST, DELETE, PUT, DEFAULT_ERROR
from . import Route
from .business import RouteBusiness

URL = '/route'
bp = Blueprint("route", "__name__", url_prefix=URL)
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
            line_id = request.args.get(Route.LINE_ID)
            if line_id:
                return _get_all_by_line(line_id)
            return _get_all()

    except Exception:
        traceback.print_exc()
        route_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)


def _get_all():
    try:
        routes = route_business.get()
        if routes:
            result = [route.to_dict() for route in routes]
            return make_response(jsonify(result))
        return make_response([])
    except Exception:
        traceback.print_exc()
        route_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)


def _get_all_by_line(line_id):
    try:
        routes = route_business.get(line_id=line_id)
        if routes:
            result = [route.to_dict() for route in routes]
            return make_response(jsonify(result))
        return make_response([])
    except Exception:
        traceback.print_exc()
        route_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)


def _get_by_id(route: Route):
    return make_response(jsonify(route.to_dict()))


def _update(current_route: Route):
    data = request.form.to_dict()
    line_id = data.get(Route.LINE_ID)
    line = line_business.get(id=line_id)
    if line:
        has_error, error_msgs = route_business.validate_fields(data, Route.FIELDS)
        if not has_error:
            new_route = Route(**data, id=id)
            route_business.update(current_route, new_route)
            return make_response(jsonify(new_route.to_dict()))
        return make_response(jsonify({'Message': error_msgs}), 400)

    return make_response({"Error": f"Line id {line_id} not found"}, 404)


@bp.route('/<int:id>', methods=[GET, DELETE, PUT])
def delete(id):
    try:
        # verificando se a Route existe
        route = route_business.get(id=id)
        if route:
            if request.method == DELETE:
                route_business.delete(id)
                return Response(status=204)

            elif request.method == GET:
                return _get_by_id(route)

            elif request.method == PUT:
                return _update(route)
        return make_response({"Message": f"Route id {id} not found"}, 404)

    except Exception:
        traceback.print_exc()
        route_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)
