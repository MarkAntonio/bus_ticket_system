import traceback

from flask import Blueprint, make_response, jsonify, request, Response

from app.util import GET, POST, DELETE, PUT, DEFAULT_ERROR
from .business import TripBusiness
from app.modules.bus.controller import bus_business
from app.modules.line.controller import line_business

from .model import Trip

ROUTE = '/trip'
bp = Blueprint("trip", "__name__", url_prefix=ROUTE)
trip_business = TripBusiness()

@bp.route("/", methods=[POST, GET])
def add():
    try:
        if request.method == POST:
            data = request.form.to_dict()
            has_error, error_msgs = trip_business.validate_fields(data, Trip.FIELDS)
            if not has_error:
                bus_id = data[Trip.BUS_ID]
                if bus_business.get(id=bus_id):
                    line_id = data[Trip.LINE_ID]
                    if line_business.get(id=line_id):
                        trip = trip_business.save(data)  # retorna o Trip com o id gerado na base
                        return make_response(jsonify(trip.to_dict()), 201)
                    return make_response(jsonify({"Message": f"Line id {line_id} not found"}), 404)
                return make_response(jsonify({"Message": f"Bus id {bus_id} not found"}), 404)

            return make_response(jsonify({'Message': error_msgs}), 400)

        elif request.method == GET:
            return _get_all()

    except Exception:
        traceback.print_exc()
        trip_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)


def _get_all():
    tripes = trip_business.get()
    if tripes:
        result = [trip.to_dict() for trip in tripes]
        return make_response(jsonify(result), 200)
    return make_response([])


def _get_by_id(id):
    trip = trip_business.get(id=id)
    if trip:
        return make_response(jsonify(trip.to_dict()), 200)
    return make_response(jsonify({"Message": "Trip id not found"}), 404)


# def _search_all_by_type(type: str):
#     tripes = trip_business.get(type=type)
#     if tripes:
#         result = [trip.to_dict() for trip in tripes]
#         return make_response(jsonify(result), 200)
#     return make_response({}, 404)


def _update(id):
    data = request.form.to_dict()
    has_error, error_msgs = trip_business.validate_fields(data, Trip.FIELDS)
    if not has_error:
        current_trip = trip_business.get(id=id)
        if current_trip:
            bus_id = data[Trip.BUS_ID]
            if bus_business.get(id=bus_id):
                line_id = data[Trip.LINE_ID]
                if line_business.get(id=line_id):
                    new_trip = Trip(**data, id=id)
                    trip_business.update(current_trip, new_trip)
                    return make_response(jsonify(new_trip.to_dict()))
                return make_response(jsonify({"Message": f"Line id {line_id} not found"}), 404)
            return make_response(jsonify({"Message": f"Bus id {bus_id} not found"}), 404)

        return make_response({"Error": "Trip id not found"}, 404)

    return make_response(jsonify({'Message': error_msgs}), 400)


@bp.route('/<int:id>', methods=[GET, DELETE, PUT])
def delete(id):
    try:
        if request.method == DELETE:
            if trip_business.get(id=id):
                trip_business.delete(id)
                return Response(status=204)
            return make_response({"Message": "Trip id not found"}, 404)
        elif request.method == GET:
            return _get_by_id(id)
        elif request.method == PUT:
            return _update(id)

    except Exception:
        traceback.print_exc()
        trip_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)
