from bson import ObjectId
from app import app


def convert_to_json_serializable(item):
    if isinstance(item, ObjectId):
        return str(item)  # Konwertuj ObjectId na łańcuch znaków
    raise TypeError(f"{type(item)} is not JSON serializable, please convert it to a string")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']