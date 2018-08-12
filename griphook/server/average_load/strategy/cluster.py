from datetime import datetime

from griphook.server.average_load.queries.common import average_load_query_builder
from griphook.server.average_load.queries.cluster import (
    get_cluster_servers_average_metric_values,
    get_cluster_server_services_query,
    get_cluster_average_metric_value,
    get_cluster_query,
)


def get_cluster_servers_metric_average_values_strategy(
        target: str, metric_type: str, time_from: datetime, time_until: datetime,
):
    """
    :param time_from: datetime
    :param time_until: datetime
    :param target: cluster_title
    :param metric_type: vsize or user_cpu_percent
    :return: average load for each server inside current server
     (only part of service which inside current services_group)
    """
    services_query_getter = get_cluster_server_services_query
    result_handler = get_cluster_servers_average_metric_values

    cluster_servers_metric_average_values = average_load_query_builder(
        target, metric_type, time_from, time_until, services_query_getter, result_handler
    )
    print(cluster_servers_metric_average_values)

    return cluster_servers_metric_average_values


def get_cluster_metric_average_value_strategy(
        target: str, metric_type: str, time_from: datetime, time_until: datetime,
):
    """
    :param time_from: datetime
    :param time_until: datetime
    :param target: cluster_title
    :param metric_type: vsize or user_cpu_percent
    """
    services_query_getter = get_cluster_query
    result_handler = get_cluster_average_metric_value

    cluster_metric_average_load = average_load_query_builder(
        target, metric_type, time_from, time_until, services_query_getter, result_handler
    )
    print(cluster_metric_average_load)
    return cluster_metric_average_load
