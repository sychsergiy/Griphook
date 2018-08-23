from cerberus import Validator


def validate_request_json(schema, request_json):
    v = Validator(schema)
    is_valid = v.validate(request_json)
    formatted_data = v.document
    return is_valid, v.errors, formatted_data
