from flask import request, jsonify

from griphook.server.billing.utils.sql_utils import billing_table_query
from griphook.server.billing.utils.formatter import output_row_formatter
from griphook.server.billing.validation.validators import validate_request_json
from griphook.server.billing.validation import schema


def get_filtered_billing_table_data():
    """
        Endpoint with average cpu and memory values for billing table.

        Incoming json:
        {
            "services_groups": [
                                "id" | integer
                                ...
                             ],
            "team": "id" | integer,
            "project": "id" | integer,
            "cluster": "id" | integer,
            "server": "id" | integer,
            "time_from": "YY-MM-DD", | required
            "time_until": "YY-MM-DD" | required

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
    valid, error_message, formatted_input_json = validate_request_json(schema.SCHEMA, request_json)
    if not valid:
        response = jsonify(error_message)
        response.status_code = 400
    else:
        result = billing_table_query(formatted_input_json)
        formatted_output = [output_row_formatter(element) for element in result]
        response = jsonify(formatted_output)
    return response
