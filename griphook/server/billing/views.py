import json

from flask import request, abort, current_app

from griphook.server.billing.utils import output_formatter, validate_request_json, billing_table_query

#
# CLUSTERS = [
# "dev", |1
# "kalm", |2...
# "olympus",
# "spark",
# "test_team_1",
# "test_team_2",
# "test_team_3"
# ]

SCHEMA = {
        "time_from": {"type": "string", "required": True},
        "time_until": {"type": "string", "required": True},
        "services_groups": {"type": "list"},
        "cluster_id": {"type": "integer"},
        "team_id": {"type": "integer"},
        "project_id": {"type": "integer"},
        "server_id": {"type": "integer"}
    }


def get_billing_table_data():
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

        "time_from" and "time_until" are mandatory fields

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

        Empty result json means the filter values were incorrect.


    """

    query_filters = request.get_json() or {}
    print(type(query_filters["time_from"]))

    valid, error_message = validate_request_json(SCHEMA, query_filters)
    if not valid:
        abort(400, error_message)

    result = billing_table_query(query_filters)
    r_list = []
    for i in result:
        pass
    result_obj = {
        "services_group_id": "value"
    }


    data = [output_formatter(element) for element in result]
    response_data = {'data': data}
    response = current_app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response






