class SqlPassenger:
    TABLE_NAME = 'passenger'
    _CREATE_TABLE = f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}(' \
                            '''id SERIAL PRIMARY KEY,
                            name VARCHAR(100) NOT NULL,
                            phone VARCHAR(14) NOT NULL CHECK (phone ~ '^\(\d{2}\)9\d{4}-\d{4}$')  
                        );'''                                           # (12)91234-1235

    _INSERT = f'''INSERT INTO {TABLE_NAME} (name, phone)
                 VALUES (%s, %s) RETURNING id;'''
    _SELECT_ALL = f'SELECT * FROM {TABLE_NAME};'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE id = {};'
    _UPDATE = '''UPDATE {} SET name = %s, phone = %s WHERE id = %s;'''
    _DELETE = 'DELETE FROM {} WHERE id = {};'
