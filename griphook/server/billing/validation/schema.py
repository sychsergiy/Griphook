from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"
ALLOWED_TARGET_TYPES = ["services_groups", "cluster", "team", "project", "server", "all"]


def modify_date(date: str):
    return datetime.strptime(date, DATE_FORMAT)


SCHEMA = {
    "target_type": {"type": "string", "allowed": ALLOWED_TARGET_TYPES, "required": True},
    "target_ids": {"type": "list", "schema": {"type": "integer"}, "empty": True, "required": True},
    "time_from": {"type": "date", "required": True, "coerce": modify_date},
    "time_until": {"type": "date", "required": True, "coerce": modify_date}
}
