def output_row_formatter(row):
    return {
            "services_group_id": row.service_group_id,
            "services_group_title": row.services_group_title,
            "team": row.team,
            "project": row.project,
            "cpu_sum": row.cpu_sum,
            "memory_sum": row.memory_sum
    }
