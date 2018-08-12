from datetime import datetime

from griphook.server.average_load.queries.group import (
    get_group_query,
    get_group_average_metric_value,

    get_group_services_query,
    get_services_average_metric_values
)

from griphook.server.average_load.queries.common import average_load_query_builder


def get_group_services_metric_average_values_strategy(
        target: str, metric_type: str, time_from: datetime, time_until: datetime, ):
    services_query_getter = get_group_services_query
    result_query_handler = get_services_average_metric_values
    return average_load_query_builder(
        target, metric_type, time_from, time_until, services_query_getter, result_query_handler
    )


def get_group_metric_average_value_strategy(target: str, metric_type: str, time_from: datetime, time_until: datetime, ):
    services_query_getter = get_group_query
    result_query_handler = get_group_average_metric_value

    group_metric_average_value = average_load_query_builder(
        target, metric_type, time_from, time_until, services_query_getter, result_query_handler
    )
    return group_metric_average_value
