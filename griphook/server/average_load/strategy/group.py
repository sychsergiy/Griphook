from datetime import datetime

from sqlalchemy import func

from griphook.server.models import (
    BatchStoryBilling,
    MetricBilling,
    Service,
    ServicesGroup,
)
from griphook.server import db


def get_group_services_metric_average_values_strategy(
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
            .filter(
            BatchStoryBilling.time >= time_from,
            BatchStoryBilling.time <= time_until,
        ).with_entities(
            ServicesGroup.title, Service.title, func.avg(MetricBilling.value)
        ).group_by(ServicesGroup.title, Service.title)
    )
    return query.all()


def get_group_metric_average_value_strategy(time_from: datetime, time_until: datetime, target: str, metric_type: str):
    query = (
        db.session.query(ServicesGroup)
            .filter(ServicesGroup.title == target)
            .join(Service)
            .join(MetricBilling)
            .filter(MetricBilling.type == metric_type)
            .join(BatchStoryBilling)
            .filter(
            BatchStoryBilling.time >= time_from,
            BatchStoryBilling.time <= time_until,
        ).with_entities(
            ServicesGroup.title, func.avg(MetricBilling.value)
        ).group_by(ServicesGroup.title)
    )
    return query.one()
