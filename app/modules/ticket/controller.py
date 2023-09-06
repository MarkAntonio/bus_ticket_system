import traceback

from flask import Blueprint, make_response, jsonify, request, Response

from app.modules.passenger.business import PassengerBusiness
from app.modules.route.business import RouteBusiness
from app.modules.seat.business import SeatBusiness
from app.modules.trip.business import TripBusiness
from app.util import GET, POST, DELETE, PUT, DEFAULT_ERROR
from .business import TicketBusiness
from .model import Ticket

ROUTE = '/ticket'
bp = Blueprint("ticket", "__name__", url_prefix=ROUTE)
ticket_business = TicketBusiness()
route_business = RouteBusiness()
passenger_business = PassengerBusiness()
seat_business = SeatBusiness()
trip_business = TripBusiness()


@bp.route("/", methods=[POST, GET])
def add():
    try:
        if request.method == POST:
            data = request.form.to_dict()
            has_error, error_msgs = ticket_business.validate_fields(data, Ticket.FIELDS)
            if not has_error:
                return _add(data)
            return make_response(jsonify({'Message': error_msgs}), 400)

        elif request.method == GET:
            return _get_all()

    except Exception:
        traceback.print_exc()
        ticket_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)
  #verficiar se aqui deve ser o código 500 (erro interno do servidor


def _add(data):
    trip_id = data[Ticket.TRIP_ID]
    trip = trip_business.get(id=trip_id)
    if trip:
        origin_id = data[Ticket.ORIGIN_ID]
        origin = route_business.get(id=origin_id)
        if origin:
            if origin.line_id != trip.line_id:
                return make_response(jsonify({"Message": f"Origin line id {origin.line_id} "
                                                         f"is not the same from trip line id {trip.line_id}"}), 404)
            destination_id = data[Ticket.DESTINATION_ID]
            destination = route_business.get(id=destination_id)
            if destination:
                if destination.line_id != trip.line_id:
                    return make_response(jsonify({"Message": f"Destination line id {destination.line_id} "
                                                             f"is not the same from trip line id {trip.line_id}"}), 404)
                if destination_id == origin_id:
                    return make_response(jsonify({"Message":
                                                      "The origin id must be different from the destination id."}), 405)
                passenger_id = data[Ticket.PASSENGER_ID]
                if passenger_business.get(id=passenger_id):
                    seat_id = data[Ticket.SEAT_ID]
                    if seat_business.get(id=seat_id):
                        # definindo o preço da rota
                        data[Ticket.ROUTE_PRICE] = abs(float(destination.price) - float(origin.price))
                        ticket = ticket_business.save(data)  # retorna o Ticket com o id gerado na base
                        return make_response(jsonify(ticket.to_dict()), 201)

                    return make_response(jsonify({"Message": f"Seat id {seat_id} not found"}), 404)
                return make_response(jsonify({"Message": f"Passenger id {passenger_id} not found"}), 404)
            return make_response(jsonify({"Message": f"Destination id {destination_id} not found"}), 404)
        return make_response(jsonify({"Message": f"Origin id {origin_id} not found"}), 404)
    return make_response(jsonify({"Message": f"Trip id {trip_id} not found"}), 404)


def _get_all():
    tickets = ticket_business.get()
    if tickets:
        result = [ticket.to_dict() for ticket in tickets]
        return make_response(jsonify(result), 200)
    return make_response([])


def _see_ticket(id):
    if ticket_business.get(id=id):
        data = ticket_business.see_ticket(id)
        if data:
            return make_response(jsonify(data), 200)
    return make_response(jsonify({"Message": "Ticket id not found"}), 404)


def __update(id, data):
    if ticket_business.get(id=id):
        trip_id = data[Ticket.TRIP_ID]
        trip = trip_business.get(id=trip_id)
        if trip:
            origin_id = data[Ticket.ORIGIN_ID]
            origin = route_business.get(id=origin_id)
            if origin:
                if origin.line_id != trip.line_id:
                    return make_response(jsonify({"Message": f"Origin line id {origin.line_id} "
                                                             f"is not the same from trip line id {trip.line_id}"}), 404)
                destination_id = data[Ticket.DESTINATION_ID]
                destination = route_business.get(id=destination_id)
                if destination:
                    if destination.line_id != trip.line_id:
                        return make_response(
                            jsonify({"Message": f"Destination line id {destination.line_id} "
                                                f"is not the same from trip line id {trip.line_id}"}), 404)
                    if destination_id == origin_id:
                        return make_response(
                            jsonify({"Message":
                                         "The origin id must be different from the destination id."}), 400)
                    passenger_id = data[Ticket.PASSENGER_ID]
                    if passenger_business.get(id=passenger_id):
                        seat_id = data[Ticket.SEAT_ID]
                        if seat_business.get(id=seat_id):
                            # definindo o preço da rota
                            data[Ticket.ROUTE_PRICE] = abs(float(destination.price) - float(origin.price))
                            ticket = ticket_business.save(data)  # retorna o Ticket com o id gerado na base
                            return make_response(jsonify(ticket.to_dict()), 201)

                        return make_response(jsonify({"Message": f"Seat id {seat_id} not found"}), 404)
                    return make_response(jsonify({"Message": f"Passenger id {passenger_id} not found"}), 404)
                return make_response(jsonify({"Message": f"Destination id {destination_id} not found"}), 404)
            return make_response(jsonify({"Message": f"Origin id {origin_id} not found"}), 404)
        return make_response(jsonify({"Message": f"Trip id {trip_id} not found"}), 404)
    return make_response(jsonify({"Message": f"Ticket id {id} not found"}), 404)


def _update(id):
    data = request.form.to_dict()
    has_error, error_msgs = ticket_business.validate_fields(data, Ticket.FIELDS)
    if not has_error:
        return __update(id, data)
    return make_response(jsonify({'Message': error_msgs}), 400)


@bp.route('/<int:id>', methods=[GET, DELETE, PUT])
def delete(id):
    try:
        if request.method == DELETE:
            if ticket_business.get(id=id):
                ticket_business.delete(id)
                return Response(status=204)
            return make_response({"Message": "Ticket id not found"}, 404)
        elif request.method == GET:
            return _see_ticket(id)
        elif request.method == PUT:
            return _update(id)

    except Exception:
        traceback.print_exc()
        ticket_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)
