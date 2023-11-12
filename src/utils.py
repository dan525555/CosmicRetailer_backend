from bson import ObjectId
from app import app


def convert_to_json_serializable(item):
    if isinstance(item, ObjectId):
        return str(item)  # Konwertuj ObjectId na łańcuch znaków
    raise TypeError(f"{type(item)} is not JSON serializable, please convert it to a string")

def serialize_object_ids(data):
    for item in data:
        for key, value in item.items():
            if isinstance(value, ObjectId):
                item[key] = convert_to_json_serializable(value)
    return data

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']