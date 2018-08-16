from griphook.server.billing.utils.formatter import modify_date

SCHEMA = {
        "time_from": {"type": "datetime", "required": True, "coerce": modify_date},
        "time_until": {"type": "datetime", "required": True, "coerce": modify_date},
        "services_groups": {"type": "list", "schema": {"type": "integer"}},
        "cluster_id": {"type": "integer"},
        "team_id": {"type": "integer"},
        "project_id": {"type": "integer"},
        "server_id": {"type": "integer"}
    }
