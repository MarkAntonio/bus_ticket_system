class SqlTicket:

    TABLE_NAME = 'ticket'
    _CREATE_TABLE = f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}(' \
                    '''	id SERIAL PRIMARY KEY,
                        trip_id SMALLINT NOT NULL REFERENCES trip(id),
                        origin_id SMALLINT NOT NULL REFERENCES route(id),
                        destination_id SMALLINT NOT NULL REFERENCES route(id),
                        passenger_id SMALLINT NOT NULL REFERENCES passenger(id),
                        seat_id VARCHAR(10) NOT NULL,
                        route_price NUMERIC(6,2) NOT NULL
                    );'''
    # Através da trip eu consigo a line_id e com a line eu consigo o bus_id
    # origin_id e destination_id servem para calcular as rotas e devem ter o mesmo line_id da trip_id
    _INSERT = f'''INSERT INTO {TABLE_NAME} (trip_id, origin_id, destination_id, passenger_id, seat_id, route_price)
                 VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;'''
    _SELECT_ALL = f'SELECT * FROM {TABLE_NAME};'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE id = {};'

    _SELECT_JOIN = '''SELECT p.name as passenger,
                        o.city as origin,
                        d.city as destination, 
                        tr.date as date,
                        o.time as time,
                        s.number as seat,
                        tr.bus_id as bus_id,
                        b.type,
                        l.origin as line_origin,
                        l.destination as line_destination,
                        t.route_price as price
                    FROM ticket t
                        INNER JOIN passenger p ON p.id = t.passenger_id
                        INNER JOIN route o ON o.id = t.origin_id
                        INNER JOIN route d ON d.id = t.destination_id
                        INNER JOIN trip tr ON tr.id = t.trip_id
                        INNER JOIN seat s ON s.id = t.seat_id
                        INNER JOIN bus b ON b.id = tr.bus_id
                        INNER JOIN line l ON l.id = tr.line_id 
                    
                    WHERE t.id = {};'''

    _SELECT_BY_PASSENGER_ID = 'SELECT * FROM {} WHERE passenger_id = {};'
    _UPDATE = 'UPDATE {} SET route_price = %s, passenger_id = %s, trip_id = %s, seat_id = %s WHERE id = %s;'
    _DELETE = 'DELETE FROM {} WHERE id = {};'
