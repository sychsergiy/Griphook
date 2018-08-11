from datetime import datetime

from griphook.server import db
from griphook.server.models import ServicesGroup, Service, MetricBilling, BatchStoryBilling

from sqlalchemy import func


def services_group_average_load_query_strategy(
        time_from: datetime, time_until: datetime, target: str, metric_type: str):
    """
    :param time_from: datetime
    :param time_until: datetime
    :param target: services_group_title
    :param metric_type: vsize or user_cpu_percent
    :return: average load for each services inside current services_group
    """
    query = (
        db.session.query(ServicesGroup)
            .filter(ServicesGroup.title == target)
            .join(Service)
            .join(MetricBilling)
            .filter(MetricBilling.type == metric_type)
            .join(BatchStoryBilling)
            .filter(BatchStoryBilling.time >= time_from, BatchStoryBilling.time <= time_until)
            .with_entities(ServicesGroup.title, Service.title, func.avg(MetricBilling.value))
            .group_by(ServicesGroup.title, Service.title)
    )
    return query.all()
