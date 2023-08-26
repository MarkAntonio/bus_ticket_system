from flask import Flask

from app.database import ConnectDataBase
from app.modules.bus.controller import bp as bp_bus
from app.modules.line.controller import bp as bp_line
from app.modules.passenger.controller import bp as bp_passenger
from app.modules.seat.controller import bp as bp_seat
from app.modules.route.controller import bp as bp_route
from app.modules.trip.controller import bp as bp_trip
from app.modules.ticket.controller import bp as bp_ticket

app = Flask(__name__)
app.register_blueprint(bp_bus)
app.register_blueprint(bp_line)
app.register_blueprint(bp_passenger)
app.register_blueprint(bp_seat)
app.register_blueprint(bp_route)
app.register_blueprint(bp_trip)
app.register_blueprint(bp_ticket)

# criando as tabelas caso não existam ainda
ConnectDataBase().init_table()  #obj anônimo

if __name__ == "__main__":
    app.run(debug=True)
