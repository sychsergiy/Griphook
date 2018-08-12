from datetime import datetime

from sqlalchemy import func

from griphook.server import db

from griphook.server.models import (
    Server,
    Service,
    ServicesGroup,
    MetricBilling,
    BatchStoryBilling,
)


def get_server_groups_metric_average_values_strategy(
        time_from: datetime, time_until: datetime, target: str, metric_type: str
):
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
            .filter(
                BatchStoryBilling.time >= time_from,
                BatchStoryBilling.time <= time_until,
            ).with_entities(
                Server.title, ServicesGroup.title, func.avg(MetricBilling.value)
            ).group_by(Server.title, ServicesGroup.title)
    )
    return query.all()


def get_server_metric_average_value_strategy(
        time_from: datetime, time_until: datetime, target: str, metric_type: str
):
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
            .filter(
                BatchStoryBilling.time >= time_from,
                BatchStoryBilling.time <= time_until,
            ).with_entities(
                Server.title, func.avg(MetricBilling.value)
            ).group_by(Server.title)
    )
    return query.one()
