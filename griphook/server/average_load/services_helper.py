from datetime import datetime

from griphook.server.models import (
    Service,
    ServicesGroup,
    MetricBilling,
    BatchStoryBilling,
)
from sqlalchemy import func


class ChartDataUtil(object):
    def __init__(self, strategy):
        self._strategy = strategy


class Strategy(object):
    def query():
        pass

    def construct_to_response():
        pass


def service_average_load_query(
    time_from: datetime, time_until: datetime, target: str, metric_type: str
):
    instances = (
        Service.query.filter(Service.title == target)
        .join(ServicesGroup)
        .join(MetricBilling)
        .filter(MetricBilling.type == metric_type)
        .join(BatchStoryBilling)
        .filter(
            BatchStoryBilling.time >= time_from,
            BatchStoryBilling.time <= time_until,
        )
        .with_entities(
            ServicesGroup.title,
            Service.title,
            Service.instance,
            func.avg(MetricBilling.value),
        )
        .group_by(ServicesGroup.title, Service.title, Service.instance)
    ).all()

    return instances
