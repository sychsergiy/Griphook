from datetime import datetime

from griphook.server import db
from griphook.server.models import Service, MetricBilling, BatchStoryBilling, Server, Cluster

from sqlalchemy import func


def cluster_average_load_query_strategy(
        time_from: datetime, time_until: datetime, target: str, metric_type: str):
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
            .filter(BatchStoryBilling.time >= time_from, BatchStoryBilling.time <= time_until)
            .with_entities(Cluster.title, Server.title, func.avg(MetricBilling.value))
            .group_by(Cluster.title, Server.title)
    )
    return query.all()
