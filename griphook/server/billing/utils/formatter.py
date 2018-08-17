from datetime import  datetime

from griphook.server.billing.constants import RESPONSE_DATE_TIME_FORMAT, REQUEST_DATE_TIME_FORMAT


def string_to_date_time(time_in_string):
    return datetime.strptime(time_in_string, REQUEST_DATE_TIME_FORMAT)


def format_output_row_for_billing_table(row):
    return {
        "services_group_id": row.service_group_id,
        "services_group_title": row.services_group_title,
        "team": row.team,
        "project": row.project,
        "cpu_sum": row.cpu_sum,
        "memory_sum": row.memory_sum
    }


def format_metrics_list_for_general_table(metrics):
    chart = {"timeline": [], "values": []}
    for metric in metrics:
        chart["timeline"].append(
            metric.time.strftime(RESPONSE_DATE_TIME_FORMAT)
        )
        chart["values"].append(round(metric.value, 1))
    return chart
