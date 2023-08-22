from . import Route
from flask import Blueprint, make_response, jsonify, request, Response
from app.util import GET, POST, DELETE, PUT, DEFAULT_ERROR
from .business import RouteBusiness
from app.modules.line.controller import line_business
import traceback

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

    except Exception:
        traceback.print_exc()
        route_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)


@bp.route('/<int:line_id>', methods=[GET])
def get_all_by_line(line_id):
    try:
        line = line_business.get(id=line_id)
        if line:
            id = request.form.get(Route.ID)
            routes = route_business.get(line_id=line_id, id=id)
            if routes:
                result = [route.to_dict() for route in routes]
                return make_response(jsonify(result))
            return make_response([])
        return make_response({"Message": f"Line id {line_id} not found"}, 404)
        print(line)
    except Exception:
        traceback.print_exc()
        route_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)


def _get_by_id(id, line_id):
    try:
        route = route_business.get(id=id, line_id=line_id)
        if route:
            return route
    except Exception:
        traceback.print_exc()
        route_business.reconnect()


def _update():
    try:
        data = request.form.to_dict()
        current_route = route_business.get(id=data.get(Route.ID), line_id=data.get(Route.LINE_ID))
        line = line_business.get(id=data.get(Route.LINE_ID))
        if line:
            if current_route:
                has_error, error_msgs = route_business.validate_fields(data, Route.FIELDS)
                if not has_error:
                    data[Route.ID] = current_route.id
                    new_route = Route(**data)
                    route_business.update(current_route, new_route)
                    return make_response(jsonify(new_route.to_dict()))
                return make_response(jsonify({'Message': error_msgs}), 400)

            return make_response({"Error": "Route id not found"}, 404)

        msg = f"Line id {data.get(Route.LINE_ID)} not found"
        return make_response({"Error": msg}, 404)


    except Exception:
        traceback.print_exc()
        route_business.reconnect()
    return jsonify(DEFAULT_ERROR)


@bp.route('/<int:line_id>', methods=[GET, DELETE, PUT])
def delete(line_id):
    try:
        id = request.form.get(Route.ID)
        if request.method == DELETE:
            # verficando se a Line existe
            if line_business.get(id=line_id):
                # verificando se a Route existe
                if route_business.get(id=id):
                    route_business.delete(id, line_id)
                    return Response(status=204)
                return make_response({"Message": f"Route id {id} not found"}, 404)
            return make_response({"Message": f"Line id {line_id} not found"}, 404)

        elif request.method == GET:
            return _get_by_id(id, line_id)
        elif request.method == PUT:
            return _update()

    except Exception:
        traceback.print_exc()
        route_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)
