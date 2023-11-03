from bson import ObjectId


def convert_to_json_serializable(item):
    if isinstance(item, ObjectId):
        return str(item)  # Konwertuj ObjectId na łańcuch znaków
    raise TypeError(f"{type(item)} is not JSON serializable, please convert it to a string")