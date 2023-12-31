class SqlSeat:

    TABLE_NAME = 'seat'
    # o id é incrementado pelo sistema, logo, não é SERIAL
    _CREATE_TABLE = f'CREATE TABLE IF NOT EXISTS seat(' \
                    '''id VARCHAR(10) NOT NULL PRIMARY KEY,
                       number SMALLINT NOT NULL,
                       is_free BOOLEAN NOT NULL,
                       vacant_in VARCHAR(50),
                       bus_id SMALLINT NOT NULL REFERENCES bus(id) ON DELETE CASCADE
                   );'''

    _INSERT = f'''INSERT INTO {TABLE_NAME} (id, number, is_free, vacant_in, bus_id)
                 VALUES (%s, %s, %s, %s, %s);'''

    # estou ordenando pelo número, pois percebi que quando atualizo um Seat ele muda de ordem no bd por não ter id.
    # Como quero sempre a ordem crescente quando eu dou um GET_ALL, por isso ordenei,
    _SELECT_ALL = 'SELECT * FROM {} where bus_id = {} ORDER BY NUMBER;'

    # Como o id é string eu tenho que colocar as aspas
    _SELECT_BY_ID = "SELECT * FROM {} WHERE id = '{}';"

    # _SELECT_BY_NUMBER = "SELECT * FROM {} WHERE bus_id={} AND number = {};"


    # o number e bus id eu não altero porque é incrementado automaticamente pelo sistema caso o ônibus exista
    _UPDATE = '''UPDATE {} SET is_free = %s, vacant_in = %s WHERE id = %s;'''

    _DELETE_ALL = 'DELETE FROM {} WHERE bus_id = {};'
