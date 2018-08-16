from flask import request, jsonify

from griphook.server.billing.utils import (
    get_services_group_metrics_group_by_services,
    validate_data_for_general_table_metrics,
    get_services_group_metrics_chart,
    format_metrics_list_to_chart,
)


def get_billing_metric_values_by_services_group():
    """
        request_json:
        {
            "services_group_id": int,
            "time_from": string,
            "time_until": string
        }

        response_json:
        [
            {
                "service_id": int,
                "service_title": string,
                "cpu": int,
                "memory": int
            }
        ]
    """
    request_json = request.get_json()
    is_valid, error_data, valid_data = validate_data_for_general_table_metrics(
        request_json
    )
    if is_valid:
        metrics = get_services_group_metrics_group_by_services(**valid_data)
        resp_data = tuple(
            {
                "cpu": metric.cpu,
                "memory": metric.memory,
                "service_id": metric.service_id,
                "service_title": metric.service_title,
            }
            for metric in metrics
        )
        response = jsonify(resp_data)
    else:
        response = jsonify(error_data)
        response.status_code = 400
    return response


def get_metric_chart_for_services_group():
    """
        request_json:
        {
            "services_group_id": int,
            "time_from": string,
            "time_until": string
        }

        response_json:
       {
            "cpu": {
                "timeline": [string],
                "values": [int]
            },
            "memory": {
                "timeline": [string],
                "values": [int]
            }
        }
    """
    request_json = request.get_json()
    is_valid, error_data, valid_data = validate_data_for_general_table_metrics(
        request_json
    )
    if is_valid:
        cpu_metrics = get_services_group_metrics_chart(
            metric_type="user_cpu_percent", **valid_data
        )
        memory_metrics = get_services_group_metrics_chart(
            metric_type="vsize", **valid_data
        )
        resp_data = {
            "cpu": format_metrics_list_to_chart(cpu_metrics),
            "memory": format_metrics_list_to_chart(memory_metrics),
        }

        response = jsonify(resp_data)
    else:
        response = jsonify(error_data)
        response.status_code = 400
    return response
