# from datetime import datetime
#
# from griphook.server.average_load.queries.common import average_load_query_builder
# from griphook.server.average_load.queries.cluster import (
#     get_cluster_servers_average_metric_values,
#     get_cluster_server_services_query,
#     get_cluster_average_metric_value,
#     get_cluster_query,
# )
#
#
# def get_cluster_servers_metric_average_values_strategy(
#         target: str, metric_type: str, time_from: datetime, time_until: datetime,
# ):
#     """
#     :param time_from: datetime
#     :param time_until: datetime
#     :param target: cluster_title
#     :param metric_type: vsize or user_cpu_percent
#     :return: average load for each server inside current server
#      (only part of service which inside current services_group)
#     """
#     services_query_getter = get_cluster_server_services_query
#     result_handler = get_cluster_servers_average_metric_values
#
#     cluster_servers_metric_average_values = average_load_query_builder(
#         target, metric_type, time_from, time_until, services_query_getter, result_handler
#     )
#     return cluster_servers_metric_average_values
#
#
# def get_cluster_metric_average_value_strategy(
#         target: str, metric_type: str, time_from: datetime, time_until: datetime,
# ):
#     """
#     :param time_from: datetime
#     :param time_until: datetime
#     :param target: cluster_title
#     :param metric_type: vsize or user_cpu_percent
#     """
#     services_query_getter = get_cluster_query
#     result_handler = get_cluster_average_metric_value
#
#     cluster_metric_average_load = average_load_query_builder(
#         target, metric_type, time_from, time_until, services_query_getter, result_handler
#     )
#     return cluster_metric_average_load

from sqlalchemy import func

from griphook.server.models import Service, Server, Cluster

from griphook.server import db


class ClusterStrategy(object):
    def __init__(self, target, metric_type, time_from, time_until):
        self.target = target
        self.metric_type = metric_type
        self.time_from = time_from
        self.time_until = time_until

    def get_cluster_server_services_query(self):
        services_query = (
            db.session.query(Cluster)
                .filter(Cluster.title == self.target)
                .join(Server)
                .join(Service)
                .with_entities(
                Cluster.title.label("cluster_title"),
                Server.title.label("server_title"),
                Service.id,
            )
        )
        return services_query

    @staticmethod
    def get_cluster_servers_average_metric_values(joined_subquery):
        aggregated_servers = (
            db.session.query(
                joined_subquery.c.cluster_title,
                joined_subquery.c.server_title,
                func.avg(joined_subquery.c.value).label("metric_average"),
            ).group_by(
                joined_subquery.c.cluster_title,
                joined_subquery.c.server_title,
            )
        )
        return aggregated_servers.all()

    def get_cluster_query(self):
        query = (
            db.session.query(Cluster)
                .filter(Cluster.title == self.target)
                .join(Server)
                .join(Service)
                .with_entities(Service.id, Cluster.title)
        )
        return query

    @staticmethod
    def get_cluster_average_metric_value(joined_subquery):
        server_average_value = (
            db.session.query(
                joined_subquery.c.title,
                func.avg(joined_subquery.c.value).label("metric_average")
            ).group_by(joined_subquery.c.title)
        )
        return server_average_value.one()
