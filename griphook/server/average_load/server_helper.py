from datetime import datetime

from griphook.server import db
from griphook.server.models import ServicesGroup, Service, MetricBilling, BatchStoryBilling, Server

from sqlalchemy import func


def server_average_load_query_strategy(
        time_from: datetime, time_until: datetime, target: str, metric_type: str):
    """
    :param time_from: datetime
    :param time_until: datetime
    :param target: server_title
    :param metric_type: vsize or user_cpu_percent
    :return: average load for each services inside current services_group
     (only part of service which inside current services_group)
    """
    query = (
        db.session.query(Server)
            .filter(Server.title == target)
            .join(Service)
            .join(ServicesGroup)
            .join(MetricBilling)
            .filter(MetricBilling.type == metric_type)
            .join(BatchStoryBilling)
            .filter(BatchStoryBilling.time >= time_from, BatchStoryBilling.time <= time_until)
            .with_entities(Server.title, ServicesGroup.title, func.avg(MetricBilling.value))
            .group_by(Server.title, ServicesGroup.title)
    )
    print(query.all())
    return query.all()
