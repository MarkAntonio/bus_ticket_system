from . import Line
from flask import Blueprint, make_response, jsonify, request, Response
from bus_ticket_system.app.util import GET, POST, DELETE, PUT, DEFAULT_ERROR
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
                return make_response(jsonify(line.to_dict()), 201)

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
        result = [line.to_dict() for line in lines]
        return make_response(jsonify(result), 200)
    return make_response([])


def _get_by_id(id):
    line = line_business.get(id=id)
    if line:
        return make_response(jsonify(line.to_dict()), 200)
    return make_response(jsonify({"Message": "Line id not found"}), 404)


def _update(id):
    current_line = line_business.get(id=id)
    data = request.form.to_dict()
    has_error, error_msgs = line_business.validate_fields(data, Line.FIELDS)
    if not has_error:
        if current_line:
            # está mostrando esse erro por que estou colocando dados de tipos diferentes de str no data
            data[Line.DEPARTURE_TIME] = Line.str_to_time(data[Line.DEPARTURE_TIME])
            data[Line.ARRIVAL_TIME] = Line.str_to_time(data[Line.ARRIVAL_TIME])
            data[Line.ID] = id
            new_line = Line(**data)
            line_business.update(current_line, new_line)
            return make_response(jsonify(new_line.to_dict()))
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
