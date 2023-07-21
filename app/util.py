from flask import Request


def validate_fields(request: Request, obj_class):
    data = request.form.to_dict()
    missing_fields = []
    for field in obj_class.FIELDS:
        if field not in data:
            missing_fields.append(field)

    if missing_fields:
        return {"Error": f"The following fields are missing or incorrect: {missing_fields}"}, False
    return data, True

def to_dict(obj):
    dict_attrs = {str(col): getattr(obj, col) for col in obj.FIELDS}
    dict_attrs["id"] = obj.id
    return dict_attrs
