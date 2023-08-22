class SqlRoute:
    TABLE_NAME = 'route'
    _CREATE_TABLE = f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}('\
                         '''id SERIAL PRIMARY KEY,
                            city VARCHAR(50) NOT NULL,
                            time Time NOT NULL,
                            price NUMERIC(6, 2) NOT NULL,
                            line_id SMALLINT NOT NULL REFERENCES line(id)
                        );'''

    _INSERT = f'''INSERT INTO {TABLE_NAME} (city, time, price, line_id)
                 VALUES (%s, %s, %s, %s) RETURNING id;'''
    _SELECT_ALL = 'SELECT * FROM {} WHERE line_id = {};'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE id = {} AND line_id = {};'
    _UPDATE = 'UPDATE {} SET city = %s, time = %s, price = %s, line_id = %s WHERE id = %s AND line_id = {};'
    _DELETE = 'DELETE FROM {} WHERE id = {} AND line_id = {};'
