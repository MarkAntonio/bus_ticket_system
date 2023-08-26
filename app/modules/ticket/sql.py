class SqlTicket:
    TABLE_NAME = 'ticket'
    _CREATE_TABLE = f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}(' \
                    '''	id SERIAL PRIMARY KEY,
                        trip_id SMALLINT NOT NULL REFERENCES trip(id),
                        origin_id SMALLINT NOT NULL REFERENCES route(id),
                        destination_id SMALLINT NOT NULL REFERENCES route(id),
                        passenger_id SMALLINT NOT NULL REFERENCES passenger(id),
                        seat_id SMALLINT[] NOT NULL,
                        route_price NUMERIC(6,2) NOT NULL
                    );'''
    # Através da trip eu consigo a line_id e com a line eu consigo o bus_id
    # origin_id e destination_id servem para calcular as rotas e devem ter o mesmo line_id da trip_id
    _INSERT = f'''INSERT INTO {TABLE_NAME} (trip_id, origin_id, destination_id, passenger_id, seat_id, route_price)
                 VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;'''
    _SELECT_ALL = f'SELECT * FROM {TABLE_NAME};'
    # _SELECT_BY_ID = 'SELECT * FROM {} WHERE id = {};'

    """
    Exemplo do Ticket
    Passageiro: Fulano
    Origem: Triunfo
    Destino: Arco Verde
    Data: 2023-09-12
    Horário: 12:30
    Poltrona: 12
    Id do ônibus: 3 
    Classe: Convencional
    Linha: Petrolina(PE) - Serra Talhada(PE)
    Preço: 
    """
    _SELECT_TICKET_JOIN = '''SELECT p.nome as passenger, 
                             FROM ticket t
                                LEFT JOIN passenger p ON p.id = t.passenger_id
                             WHERE id = {}'''

    _SELECT_BY_PASSENGER_ID = 'SELECT * FROM {} WHERE passenger_id = {};'
    _UPDATE = 'UPDATE {} SET route_price = %s, passenger_id = %s, trip_id = %s, seat_id = %s WHERE id = %s;'
    _DELETE = 'DELETE FROM {} WHERE id = {};'
    # _SEARCH_BY_ROUTE = "SELECT * FROM {} WHERE type ILIKE '%{}%';" # quero todos por tipo
