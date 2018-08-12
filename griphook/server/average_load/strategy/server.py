from datetime import datetime

from griphook.server.average_load.queries.server import (
    get_server_average_metric_value,
    get_server_query,
    get_server_groups_average_metric_values,
    get_server_groups_services_query
)

from griphook.server.average_load.queries.common import average_load_query_builder


def get_server_groups_metric_average_values_strategy(
        target: str, metric_type: str, time_from: datetime, time_until: datetime,
):
    """
    :param time_from: datetime
    :param time_until: datetime
    :param target: server_title
    :param metric_type: vsize or user_cpu_percent
    :return: average load for each services inside current services_group
     (only part of service which inside current services_group)
    """
    services_query_getter = get_server_groups_services_query
    result_handler = get_server_groups_average_metric_values

    server_groups_metric_average_values = average_load_query_builder(
        target, metric_type, time_from, time_until, services_query_getter, result_handler
    )
    return server_groups_metric_average_values


def get_server_metric_average_value_strategy(
        target: str, metric_type: str, time_from: datetime, time_until: datetime,
):
    """
    :param time_from: datetime
    :param time_until: datetime
    :param target: server_title
    :param metric_type: vsize or user_cpu_percent
    :return: average load for each services inside current services_group
     (only part of service which inside current services_group)
    """
    services_query_getter = get_server_query
    result_handler = get_server_average_metric_value

    server_average_metric_value = average_load_query_builder(
        target, metric_type, time_from, time_until, services_query_getter, result_handler
    )

    return server_average_metric_value
