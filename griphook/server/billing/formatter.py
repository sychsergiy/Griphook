from datetime import datetime

from griphook.server.billing.constants import (
    RESPONSE_DATE_TIME_FORMAT,
    REQUEST_DATE_TIME_FORMAT,
)


def string_to_date_time(time_in_string):
    return datetime.strptime(time_in_string, REQUEST_DATE_TIME_FORMAT)


def format_row_for_billing_table(row):
    return {
        "services_group_id": row.service_group_id,
        "services_group_title": row.services_group_title,
        "team": row.team,
        "project": row.project,
        "cpu_sum": round(row.cpu_sum, 0),
        "memory_sum": round(row.memory_sum, 0)
    }


def format_metrics_list_for_general_table(metrics):
    chart = {"timeline": [], "values": []}
    for metric in metrics:
        chart["timeline"].append(
            metric.time.strftime(RESPONSE_DATE_TIME_FORMAT)
        )
        chart["values"].append(round(metric.value, 0))
    return chart
