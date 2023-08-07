from flask import Request

POST = "POST"
GET = "GET"
DELETE = "DELETE"
PUT = "PUT"


class BaseValidate:
    def validate_fields(self, data, required_fields):
        error_msgs = []  # serão as mensagens de erro
        error_flag = False  # diz se tem erro ou não
        missing_fields = []

        for field in required_fields:
            if field not in data:
                missing_fields.append(field)
        if missing_fields:
            error_flag = True
            error_msgs.append(f"The following fields are missing or the keys are incorrect: {missing_fields}")

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


def to_dict(obj):
    dict_attrs = {str(col): getattr(obj, col) for col in obj.FIELDS}
    dict_attrs["id"] = obj.id
    return dict_attrs
