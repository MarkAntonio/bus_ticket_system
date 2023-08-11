from . import Line
from flask import Blueprint, make_response, jsonify, request, Response
from bus_ticket_system.app.util import to_dict, GET, POST, DELETE, PUT, DEFAULT_ERROR
from .business import LineBusiness
import traceback

ROUTE = '/line'
bp = Blueprint("line", "__name__", url_prefix=ROUTE)
line_business = LineBusiness()


@bp.route("/", methods=[POST, GET])
def add():
    try:
        if request.method == POST:
            data = request.form.to_dict()
            has_error, error_msgs = line_business.validate_fields(data, Line.FIELDS)
            if not has_error:
                line = line_business.save(data)  # retorna o Line com o id gerado na base
                return make_response(jsonify(to_dict(line)), 201)

            return make_response(jsonify({'Message': error_msgs}), 400)

        elif request.method == GET:
            return _get_all()

    except Exception:
        traceback.print_exc()
        line_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)


def _get_all():
    lines = line_business.get()
    if lines:
        result = [to_dict(line) for line in lines]
        print(result)
        return make_response(jsonify(result), 200)
    return make_response([])


def _get_by_id(id):
    line = line_business.get(id=id)
    if line:
        return make_response(jsonify(to_dict(line)), 200)
    return make_response(jsonify({"Message": "Line id not found"}), 404)


def _update(id):
    current_line = line_business.get(id=id)
    data = request.form.to_dict()
    has_error, error_msgs = line_business.validate_fields(data, Line.FIELDS)
    if not has_error:
        if current_line:
            new_line = Line(**data, id=id)
            line_business.update(current_line, new_line)
            return make_response(jsonify(to_dict(new_line)))
        return make_response({"Error": "Line id not found"}, 404)

    return make_response(jsonify({'Message': error_msgs}), 400)


@bp.route('/<int:id>', methods=[GET, DELETE, PUT])
def delete(id):
    try:
        if request.method == DELETE:
            if line_business.get(id=id):
                line_business.delete(id)
                return Response(status=204)
            return make_response({"Message": "Line id not found"}, 404)
        elif request.method == GET:
            return _get_by_id(id)
        elif request.method == PUT:
            return _update(id)

    except Exception:
        traceback.print_exc()
        line_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)
