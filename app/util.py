from app.database import ConnectDataBase

POST = "POST"
GET = "GET"
DELETE = "DELETE"
PUT = "PUT"
DEFAULT_ERROR = {'Message': 'Ocorreu um erro. Tente novamente ou fale com o suporte.'}


class BaseValidate:
    def validate_fields(self, data: dict, required_fields: list):
        error_msgs = []  # serão as mensagens de erro
        error_flag = False  # diz se tem erro ou não
        missing_fields = []
        # verifica se a request terá os campos obrigatórios
        for field in required_fields:
            if field not in data or len(data) == 0:
                missing_fields.append(field)

        # Verifica se os valores dos campos não estão vazios.
        for key, value in data.items():
            if value.replace(' ', '') == "":
                missing_fields.append(key)

        if missing_fields:
            error_flag = True
            error_msgs.append(f"The following values are missing or the keys are incorrect: {missing_fields}")

        for field in required_fields:
            if field not in missing_fields:
                # get e has attr vão servir verificar se existe e se sim pegar o método específico da classe que herdar dessa
                method_name = '_validate_{}'.format(field)  # cria a string que representa o nome do método
                method = hasattr(self, method_name)  # revifica se o método existe e retorna um boleano
                if method:
                    method = getattr(self, method_name)  # pega o método
                    data_value = method(data.get(field, None))  # chama o método passando o parâmetro
                    if data_value is not None:
                        error_msgs.append(data_value)
                        error_flag = True
        return error_flag, error_msgs


class BaseDAO:
    def __init__(self):
        self.connection = ConnectDataBase().get_instance()

    # método save está desenvolvido parcialmente e deve ser finalizado na classe que o herdar de acordo com a necessidade
    # lembrando sempre de fechar o cursor
    def _save(self, sql, obj_tuple):
        cursor = self.connection.cursor()
        cursor.execute(sql, obj_tuple)
        self.connection.commit()
        return cursor

    def _get_all(self, sql, Obj_class):
        objects = []
        cursor = self.connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]

        for row in result:
            objects.append(self._create_object(columns_name, row, Obj_class))

        cursor.close()
        if objects:
            return objects

    def _get_by(self, sql: str, Obj_class):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        if row:
            columns_name = [desc[0] for desc in cursor.description]
            cursor.close()
            bus = self._create_object(columns_name, row, Obj_class)
            return bus

    def _create_object(self, columns_name, data, Obj_class):
        if data:
            data = dict(zip(columns_name, data))
            return Obj_class(**data)
        return None

    def _update(self, sql, objetcs_tuple: tuple):
        cursor = self.connection.cursor()
        cursor.execute(sql, objetcs_tuple)
        self.connection.commit()
        cursor.close()

    def _delete(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def rollback(self):
        self.connection.rollback()
