class SqlTrip:
    TABLE_NAME = 'trip'
    _CREATE_TABLE = f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}(' \
                         '''id SERIAL PRIMARY KEY,
                            date DATE NOT NULL,
                            line_id SMALLINT NOT NULL REFERENCES line(id) ON DELETE CASCADE,
                            bus_id SMALLINT NOT NULL REFERENCES bus(id) ON DELETE SET NULL
                        );'''

    _INSERT = f'''INSERT INTO {TABLE_NAME} (date, line_id, bus_id)
                 VALUES (%s, %s, %s) RETURNING id;'''
    _SELECT_ALL = f'SELECT * FROM {TABLE_NAME};'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE id = {};'
    _UPDATE = 'UPDATE {} SET date = %s, line_id = %s, bus_id = %s WHERE id = %s;'
    _DELETE = 'DELETE FROM {} WHERE id = {};'
    # _SEARCH_BY_ROUTE = "SELECT * FROM {} WHERE type ILIKE '%{}%';" # quero todos por tipo
