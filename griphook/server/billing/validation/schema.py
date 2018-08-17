from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"


def modify_date(date: str) -> datetime:
    return datetime.strptime(date, DATE_FORMAT)


SCHEMA = {
    "time_from": {"type": "datetime", "required": True, "coerce": modify_date},
    "time_until": {"type": "datetime", "required": True, "coerce": modify_date},
    "services_groups": {"type": "list", "schema": {"type": "integer"}},
    "cluster_id": {"type": "integer"},
    "team_id": {"type": "integer"},
    "project_id": {"type": "integer"},
    "server_id": {"type": "integer"}
    }
