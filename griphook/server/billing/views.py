import json

from flask import request, abort, current_app
from sqlalchemy import func
from sqlalchemy.sql import label

from griphook.server.models import MetricBilling, Team, Project, BatchStoryBilling, Service, ServicesGroup

from griphook.server.billing.utils import modify_time, raw_output_formatter


def get_billing_table_data():
    """
        Endpoint with average cpu and memory values for billing table.

        Incoming json:
        {
            "service_group": [
                                "value"
                                ...
                             ],
            "team": "value",
            "project": "value",
            "cluster": "value",
            "server": "value",
            "time_from": "value",
            "time_until": "value"

        }

        "time_from" and "time_until" are mandatory fields

        Result json:
        [
            {
                "service_group": "value",
                "team": "value",
                "project": "value",
                "cpu": "value",
                "memory": "value
            }
            ...
        ]

        If there are no filters (except for time_from and time_until),
        return all service groups with average cpu and memory
    """


    """
    select 
	services_groups.title,
	metrics_billing.type,
	sum(metrics_billing.value)
	
    from services_groups 
    join services on services_groups.id = services.id
    join metrics_billing on services_groups.id = metrics_billing.services_group_id
    where services_groups.title = 'zk-customers-trunk'
    group by 1,2;
    
    """
    print(request.get_json())
    query_filters = request.get_json() or {}
    time_from = modify_time(query_filters.get("time_from", None))
    time_until = modify_time(query_filters.get("time_until", None))
    print(str(request.args))
    print("time from", time_from)
    if not time_from or not time_until:
        abort(400)

    query = (
        ServicesGroup.query
        .with_entities(
            label("service_group", ServicesGroup.title),
            # label("team", Team.title),
            # label("project", Project.title),
            label("metric_type", MetricBilling.type),
            label("value", func.sum(MetricBilling.value))
        )
        .join(MetricBilling, MetricBilling.services_group_id == ServicesGroup.id)
        # .join(Team, Team.id == ServicesGroup.team_id)
        # .join(Project, Project.id == ServicesGroup.project_id)
        .join(BatchStoryBilling, BatchStoryBilling.id == MetricBilling.batch_id)
        .filter(BatchStoryBilling.time.between(time_from, time_until))
        # exclude system_cpu_percent from the query as we don't need it
        .filter(MetricBilling.type != 'system_cpu_percent')
        .group_by('service_group', 'metric_type',)
    )

    print("Query:", query.all())

    data = [raw_output_formatter(element) for element in query.all()]
    response_data = {'data': data}
    response = current_app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response






