from flask import Flask
from bus_ticket_system.app.database import ConnectDataBase
from bus_ticket_system.app.modules.bus.controller import bp as bp_bus
from bus_ticket_system.app.modules.line.controller import bp as bp_line
from bus_ticket_system.app.modules.passenger.controller import bp as bp_passenger

app = Flask(__name__)
app.register_blueprint(bp_bus)
app.register_blueprint(bp_line)
app.register_blueprint(bp_passenger)



# criando as tabelas caso não existam ainda
ConnectDataBase().init_table()  #obj anônimo

if __name__ == "__main__":
    app.run(debug=True)
