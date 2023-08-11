class SqlBus:
    TABLE_NAME = 'bus'
    _CREATE_TABLE = f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}(' \
                            '''id SERIAL PRIMARY KEY,
                            license_plate CHAR(7) NOT NULL UNIQUE CHECK (license_plate ~ '[A-Z]{3}[0-9][A-Z][0-9]{2}'),
                            type VARCHAR(12) 
                            CHECK (type IN ('Convencional', 'Executivo', 'Semi Leito', 'Leito', 'Leito Cama')),
                            amount_seats INTEGER NOT NULL
                        );'''

    _INSERT = f'''INSERT INTO {TABLE_NAME} (license_plate, type, amount_seats)
                 VALUES (%s, %s, %s) RETURNING id;'''
    _SELECT_ALL = f'SELECT * FROM {TABLE_NAME};'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE id = {};'
    _UPDATE = 'UPDATE {} SET license_plate = %s, type = %s, amount_seats = %s WHERE id = %s;'
    _DELETE = 'DELETE FROM {} WHERE id = {};'
    _SELECT_BY_LICENSE = "SELECT * FROM {} WHERE license_plate = '{}';"  # Quero somente uma placa
    _SEARCH_TYPES = "SELECT * FROM {} WHERE type ILIKE '%{}%';" # quero todos por tipo
