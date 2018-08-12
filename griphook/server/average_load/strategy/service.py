from griphook.server.average_load.queries.common import average_load_query_builder
from griphook.server.average_load.queries.service import (
    get_instances_average_metric_values,
    get_service_average_metric_value,
    get_service_instances_query,
    get_service_query
)


def get_service_instances_metric_average_values_strategy(target, metric_type, time_from, time_until):
    services_subquery_getter = get_service_instances_query
    result_query_handler = get_instances_average_metric_values

    aggregated_instances = average_load_query_builder(
        target, metric_type, time_from, time_until, services_subquery_getter, result_query_handler
    )
    return aggregated_instances


def get_service_metric_average_value_strategy(target, metric_type, time_from, time_until):
    services_subquery_getter = get_service_query
    result_query_handler = get_service_average_metric_value

    service_average_metric_value = average_load_query_builder(
        target, metric_type, time_from, time_until, services_subquery_getter, result_query_handler
    )
    return service_average_metric_value
