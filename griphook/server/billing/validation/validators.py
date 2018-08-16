from cerberus import Validator

from griphook.server.billing.utils.formatter import modify_date


def is_valid_date_format(request_json: dict) -> bool:
    is_valid_time_from = is_correct_time_format(request_json.get("time_from", None))
    is_valid_time_until = is_correct_time_format(request_json.get("time_until", None))
    return is_valid_time_from and is_valid_time_until


def validate_request_json(schema: dict, request_json: dict) -> (bool, dict):
    v = Validator(schema)
    if not (v.validate(request_json) and is_valid_date_format(request_json)):
        return False, v.errors
    return True


def is_correct_time_format(raw_date) -> bool:
    try:
        modify_date(raw_date)
    except ValueError:
        return False
    except TypeError:
        return False
    return True

