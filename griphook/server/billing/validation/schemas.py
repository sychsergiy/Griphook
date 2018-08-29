from griphook.server.billing.formatter import string_to_date_time
from griphook.server.billing.constants import ALLOWED_TARGET_TYPES, ALLOWED_METRIC_TYPES

SCHEMA_FOR_BILLING_TABLE = {
    "page": {"type": "integer", "required": True, "min": 1},
    "target_type": {
        "type": "string",
        "allowed": tuple(ALLOWED_TARGET_TYPES.values()),
        "required": True,
    },
    "target_ids": {
        "type": "list",
        "schema": {"type": "integer"},
        "empty": True,
        "required": True,
    },
    "time_from": {"type": "date", "required": True, "coerce": string_to_date_time},
    "time_until": {"type": "date", "required": True, "coerce": string_to_date_time},
}

BILLING_TABLE_SERVICES_GROUP_SCHEMA = {
    "services_group_id": {"type": "integer", "required": True},
    "time_from": {"type": "date", "required": True, "coerce": string_to_date_time},
    "time_until": {"type": "date", "required": True, "coerce": string_to_date_time},
}

BILLING_TABLE_SERVICES_GROUP_CHART_SCHEMA = {
    "services_group_id": {"type": "integer", "required": True},
    "time_from": {"type": "date", "required": True, "coerce": string_to_date_time},
    "time_until": {"type": "date", "required": True, "coerce": string_to_date_time},
    "metric_type": {
        "type": "string",
        "required": True,
        "allowed": tuple(ALLOWED_METRIC_TYPES.values()),
    },
}

PIE_CHART_ENDPOINT_SCHEMA = {
    "target_type": {
        "type": "string",
        "allowed": tuple(ALLOWED_TARGET_TYPES.values()),
        "required": True,
    },
    "target_ids": {
        "type": "list",
        "schema": {"type": "integer"},
        "empty": True,
        "required": True,
    },
    "metric_type": {
        "type": "string",
        "required": True,
        "allowed": tuple(ALLOWED_METRIC_TYPES.values()),
    },
    "time_from": {"type": "date", "required": True, "coerce": string_to_date_time},
    "time_until": {"type": "date", "required": True, "coerce": string_to_date_time},
}
