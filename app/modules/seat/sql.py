class SqlSeat:
    TABLE_NAME = 'seat'
    _CREATE_TABLE = f'CREATE TABLE IF NOT EXISTS seat('\
                            '''id SERIAL PRIMARY KEY,
                            is_free BOOLEAN NOT NULL,
                            vacant_in VARCHAR(50),
                            bus_id SMALLINT NOT NULL REFERENCES bus(id) 
                        );'''

    _INSERT = f'''INSERT INTO {TABLE_NAME} (is_free, vacant_in, bus_id)
                 VALUES (%s, %s, %s);'''
    _SELECT_ALL = 'SELECT * FROM {} where bus_id = {};'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE id = {};'

    # o bus id eu não altero porque é incrementado automaticamente pelo sistema caso o ônibus exista
    _UPDATE = '''UPDATE {} SET is_free = %s, vacant_in = %s WHERE id = %s;'''

    _DELETE_ALL = 'DELETE FROM {} WHERE bus_id = {};'
