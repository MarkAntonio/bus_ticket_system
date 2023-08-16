class SqlSeat:

    TABLE_NAME = 'seat'
    # o number é como se fosse o id, mas ele pode se repetir na table, pois, o deve diferenciar é o bus id
    # pois dois ônibus podem ter uma poltrona de numeração 22, por exemplo.
    _CREATE_TABLE = f'CREATE TABLE IF NOT EXISTS seat(' \
                    '''number SMALLINT NOT NULL,
                       is_free BOOLEAN NOT NULL,
                       vacant_in VARCHAR(50),
                       bus_id SMALLINT NOT NULL REFERENCES bus(id) 
                   );'''

    _INSERT = f'''INSERT INTO {TABLE_NAME} (number, is_free, vacant_in, bus_id)
                 VALUES (%s, %s, %s, %s);'''
    _SELECT_ALL = 'SELECT * FROM {} where bus_id = {};'
    _SELECT_BY_NUMBER = 'SELECT * FROM {} WHERE number = {} and bus_id = {};'

    # o number e bus id eu não altero porque é incrementado automaticamente pelo sistema caso o ônibus exista
    _UPDATE = '''UPDATE {} SET is_free = %s, vacant_in = %s WHERE number = %s;'''

    _DELETE_ALL = 'DELETE FROM {} WHERE bus_id = {};'
