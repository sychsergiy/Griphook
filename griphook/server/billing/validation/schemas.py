from griphook.server.billing.utils.formatter import string_to_date_time
from griphook.server.billing.constants import (
    ALLOWED_TARGET_TYPES_FOR_BILLING_TABLE
)

SCHEMA_FOR_BILLING_TABLE = {
    "target_type": {
        "type": "string",
        "allowed": ALLOWED_TARGET_TYPES_FOR_BILLING_TABLE,
        "required": True,
    },
    "target_ids": {
        "type": "list",
        "schema": {"type": "integer"},
        "empty": True,
        "required": True,
    },
    "time_from": {
        "type": "date",
        "required": True,
        "coerce": string_to_date_time,
    },
    "time_until": {
        "type": "date",
        "required": True,
        "coerce": string_to_date_time,
    },
}

SCHEMA_FOR_GENERAL_TABLE = {
    "services_group_id": {"type": "integer", "required": True},
    "time_from": {
        "type": "date",
        "required": True,
        "coerce": string_to_date_time,
    },
    "time_until": {
        "type": "date",
        "required": True,
        "coerce": string_to_date_time,
    },
}
