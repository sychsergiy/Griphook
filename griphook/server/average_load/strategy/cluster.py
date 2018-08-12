from datetime import datetime

from sqlalchemy import func

from griphook.server import db

from griphook.server.models import (
    Server,
    Service,
    MetricBilling,
    BatchStoryBilling,
    Cluster,
)


def get_cluster_servers_metric_average_values_strategy(
        time_from: datetime, time_until: datetime, target: str, metric_type: str
):
    """
    :param time_from: datetime
    :param time_until: datetime
    :param target: cluster_title
    :param metric_type: vsize or user_cpu_percent
    :return: average load for each server inside current server
     (only part of service which inside current services_group)
    """
    query = (
        db.session.query(Cluster)
            .filter(Cluster.title == target)
            .join(Server)
            .join(Service)
            .join(MetricBilling)
            .filter(MetricBilling.type == metric_type)
            .join(BatchStoryBilling)
            .filter(
            BatchStoryBilling.time >= time_from,
            BatchStoryBilling.time <= time_until,
        )
            .with_entities(Cluster.title, Server.title, func.avg(MetricBilling.value))
            .group_by(Cluster.title, Server.title)
    )
    return query.all()


def get_cluster_metric_average_value_strategy(
        time_from: datetime, time_until: datetime, target: str, metric_type: str
):
    """
    :param time_from: datetime
    :param time_until: datetime
    :param target: cluster_title
    :param metric_type: vsize or user_cpu_percent
    """
    query = (
        db.session.query(Cluster)
            .filter(Cluster.title == target)
            .join(Server)
            .join(Service)
            .join(MetricBilling)
            .filter(MetricBilling.type == metric_type)
            .join(BatchStoryBilling)
            .filter(
            BatchStoryBilling.time >= time_from,
            BatchStoryBilling.time <= time_until,
        )
            .with_entities(Cluster.title, func.avg(MetricBilling.value))
            .group_by(Cluster.title)
    )
    return query.one()
