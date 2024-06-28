from uuid import uuid4
def get_obligatory_fields(model):
    ob_fields = []
    for column in model.__table__.columns:
        if not column.nullable and not column.primary_key:
            ob_fields.append(column.name)
    return ob_fields

def uuid_to_str():
    return str(uuid4())
