import traceback

from flask import Blueprint, make_response, jsonify, request, Response

from app.util import GET, POST, DELETE, PUT, DEFAULT_ERROR
from .business import TicketBusiness
from app.modules.bus.controller import bus_business
from app.modules.line.controller import line_business

from .model import Ticket

ROUTE = '/ticket'
bp = Blueprint("ticket", "__name__", url_prefix=ROUTE)
ticket_business = TicketBusiness()

@bp.route("/", methods=[POST, GET])
def add():
    try:
        if request.method == POST:
            data = request.form.to_dict()
            has_error, error_msgs = ticket_business.validate_fields(data, Ticket.FIELDS)
            if not has_error:
                bus_id = data[Ticket.BUS_ID]
                if bus_business.get(id=bus_id):
                    line_id = data[Ticket.LINE_ID]
                    if line_business.get(id=line_id):
                        ticket = ticket_business.save(data)  # retorna o Ticket com o id gerado na base
                        return make_response(jsonify(ticket.to_dict()), 201)
                    return make_response(jsonify({"Message": f"Line id {line_id} not found"}), 404)
                return make_response(jsonify({"Message": f"Bus id {bus_id} not found"}), 404)

            return make_response(jsonify({'Message': error_msgs}), 400)

        elif request.method == GET:
            return _get_all()

    except Exception:
        traceback.print_exc()
        ticket_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)


def _get_all():
    ticketes = ticket_business.get()
    if ticketes:
        result = [ticket.to_dict() for ticket in ticketes]
        return make_response(jsonify(result), 200)
    return make_response([])


def _get_by_id(id):
    ticket = ticket_business.get(id=id)
    if ticket:
        return make_response(jsonify(ticket.to_dict()), 200)
    return make_response(jsonify({"Message": "Ticket id not found"}), 404)


def _update(id):
    data = request.form.to_dict()
    has_error, error_msgs = ticket_business.validate_fields(data, Ticket.FIELDS)
    if not has_error:
        current_ticket = ticket_business.get(id=id)
        if current_ticket:
            bus_id = data[Ticket.BUS_ID]
            if bus_business.get(id=bus_id):
                line_id = data[Ticket.LINE_ID]
                if line_business.get(id=line_id):
                    new_ticket = Ticket(**data, id=id)
                    ticket_business.update(current_ticket, new_ticket)
                    return make_response(jsonify(new_ticket.to_dict()))
                return make_response(jsonify({"Message": f"Line id {line_id} not found"}), 404)
            return make_response(jsonify({"Message": f"Bus id {bus_id} not found"}), 404)

        return make_response({"Error": "Ticket id not found"}, 404)

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
            return _get_by_id(id)
        elif request.method == PUT:
            return _update(id)

    except Exception:
        traceback.print_exc()
        ticket_business.reconnect()
    return make_response(jsonify(DEFAULT_ERROR), 404)
