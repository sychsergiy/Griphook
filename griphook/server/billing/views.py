from flask import request, jsonify

from griphook.server.billing.utils.sql_utils import (
    billing_table_query,
    get_services_group_metrics_chart,
    get_services_group_metrics_group_by_services,
)
from griphook.server.billing.utils.formatter import (
    format_output_row_for_billing_table,
    format_metrics_list_for_general_table,
)
from griphook.server.billing.validation import validators
from griphook.server.billing.validation import schemas


def get_filtered_billing_table_data():
    """
        Endpoint with average cpu and memory values for billing table.

        Incoming json:
        {
            "target_type": string, | required
            "target_ids": list of integers, | can be empty
            "time_from": string, | required
            "time_until": string, | required
        }


        time_from and time_until are mandatory fields

        If there are no filters (except for time_from and time_until),
        return all service groups with average cpu and memory

        Result json:
        [
            {
                "services_group_id": "id" | integer
                "services_group": "title" | string,
                "team": "title" | string,
                "project": "title" | string,
                # TODO: evaluate cpu
                # "cpu_sum": "value" | float,
                "memory_sum": "value" | integer
            }
            ...
        ]
    """

    request_json = request.get_json() or {}
    valid, error_message, formatted_input_json = validators.validate_request_json_for_billing_table(
        schemas.SCHEMA_FOR_BILLING_TABLE, request_json
    )

    if not valid:
        response = jsonify(error_message)
        response.status_code = 400
    else:
        result = billing_table_query(formatted_input_json)
        formatted_output = [
            format_output_row_for_billing_table(element) for element in result
        ]
        response = jsonify(formatted_output)
    return response


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
    is_valid, error_data, valid_data = validators.validate_request_json_for_general_table(
        schemas.SCHEMA_FOR_GENERAL_TABLE, request_json
    )
    if is_valid:
        metrics = get_services_group_metrics_group_by_services(**valid_data)
        resp_data = tuple(
            {
                "cpu": round(metric.cpu, 1),
                "memory": round(metric.memory, 1),
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
    is_valid, error_data, valid_data = validators.validate_request_json_for_general_table(
        schemas.SCHEMA_FOR_GENERAL_TABLE, request_json
    )
    if is_valid:
        cpu_metrics = get_services_group_metrics_chart(
            metric_type="user_cpu_percent", **valid_data
        )
        memory_metrics = get_services_group_metrics_chart(
            metric_type="vsize", **valid_data
        )
        resp_data = {
            "cpu": format_metrics_list_for_general_table(cpu_metrics),
            "memory": format_metrics_list_for_general_table(memory_metrics),
        }

        response = jsonify(resp_data)
    else:
        response = jsonify(error_data)
        response.status_code = 400
    return response
