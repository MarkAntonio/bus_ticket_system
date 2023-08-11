from bus_ticket_system.app.modules.bus.sql import SqlBus


class SqlSeat:
    TABLE_NAME = 'seat'
    _CREATE_TABLE = f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
                            id SERIAL PRIMARY KEY,
                            is_free BOOLEAN NOT NULL,
                            vacant_in VARCHAR(50),
                            bus_id SMALLINT NOT NULL REFERENCES {SqlBus.TABLE_NAME}(id)
                        );'''

    _INSERT = f'''INSERT INTO {TABLE_NAME} (is_free, vacant_in, bus_id)
                 VALUES (%s, %s, %s) RETURNING id;'''
    _SELECT_ALL = f'SELECT * FROM {TABLE_NAME};' # precisarei para saber quais são todos os disponíveis ou não

    # _SELECT_BY_ID = 'SELECT * FROM {} WHERE id = {};' esse não é necessário pois, quando vamos escolher
    # assentos queremos ver todos os disponíveis
    # _UPDATE = 'UPDATE {} SET is_free = %s, vacant_in = %s, bus_id = %s WHERE id = %s;' como será incrementado
    # automaticamente pelo sistema, não deve existir erros ou necessidade de atualizar o id do ônibus.

    _SET_OCCUPIED = 'UPDATE {} SET is_free = %s, vacant_in = %s WHERE id = %s;'
    _DELETE = 'DELETE FROM {} WHERE id = {};'
    _SELECT_FREE = f'SELECT * FROM {TABLE_NAME} WHERE is_free = TRUE;'  # Todos os assentos que estão livres
