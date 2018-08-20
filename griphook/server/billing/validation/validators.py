from cerberus import Validator


def validate_request_json_for_billing_table(schema, request_json):
    v = Validator(schema)
    is_valid = v.validate(request_json)
    error_message = v.errors
    formatted_data = v.document
    return is_valid, error_message, formatted_data


def validate_request_json_for_general_table(schema, request_json):
    v = Validator(schema)
    is_valid = v.validate(request_json)
    formatted_data = v.document
    return is_valid, v.errors, formatted_data
