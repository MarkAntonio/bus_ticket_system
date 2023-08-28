class SqlLine:
    TABLE_NAME = 'line'
    _CREATE_TABLE = f'''CREATE TABLE IF NOT EXISTS line(
                            id SERIAL PRIMARY KEY,
                            origin VARCHAR(50) NOT NULL,
                            destination VARCHAR(50) NOT NULL,
                            departure_time TIME NOT NULL,
                            arrival_time TIME NOT NULL,
                            total_price NUMERIC(6,2) NOT NULL
                        );'''

    _INSERT = f'''INSERT INTO {TABLE_NAME} (origin, destination, departure_time, arrival_time, total_price)
                 VALUES (%s, %s, %s, %s, %s) RETURNING id;'''
    _SELECT_ALL = f'SELECT * FROM {TABLE_NAME};'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE id = {};'
    _UPDATE = '''UPDATE {} SET origin = %s, destination = %s, 
                 departure_time = %s, arrival_time = %s, routes = %s, total_price = %s WHERE id = %s;'''
    _DELETE = 'DELETE FROM {} WHERE id = {};'
