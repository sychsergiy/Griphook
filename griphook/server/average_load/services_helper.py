from datetime import datetime

from griphook.server.models import (
    Service,
    ServicesGroup,
    MetricBilling,
    BatchStoryBilling,
)
from sqlalchemy import func

from griphook.server import db


class ChartDataUtargettil(object):
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
    instances_subquery = get_services_query(target).subquery()
    batch_story_subquery = get_batch_story_query(
        time_from, time_until
    ).subquery()
    metric_subquery = get_metric_billing_query(metric_type).subquery()

    aggregated_instances = get_services_average_metric_value(
        instances_subquery, batch_story_subquery, metric_subquery
    )
    return aggregated_instances


def get_services_average_metric_value(
    instances_subquery, batch_story_subquery, metric_subquery
):
    aggregated_instances = (
        db.session.query(instances_subquery)
        .join(metric_subquery)
        .join(batch_story_subquery)
        .with_entities(
            instances_subquery.c.services_group_title,
            instances_subquery.c.service_title,
            instances_subquery.c.instance,
            func.avg(metric_subquery.c.value).label("average_" + "metric_type"),
        )
        .group_by(
            instances_subquery.c.services_group_title,
            instances_subquery.c.service_title,
            instances_subquery.c.instance,
        )
    ).all()
    return aggregated_instances


def get_metric_billing_query(metric_type):
    query = (
        db.session.query(MetricBilling)
        .filter(MetricBilling.type == metric_type)
        .with_entities(
            MetricBilling.id,
            MetricBilling.value,
            MetricBilling.batch_id,
            MetricBilling.service_id,
        )
    )
    return query


def get_batch_story_query(time_from, time_until):
    query = (
        db.session.query(BatchStoryBilling)
        .filter(
            BatchStoryBilling.time >= time_from,
            BatchStoryBilling.time <= time_until,
        )
        .with_entities(BatchStoryBilling.id)
    )
    return query


def get_services_query(service_title):
    instances_query = (
        db.session.query(Service)
        .filter(Service.title == service_title)
        .join(ServicesGroup)
        .with_entities(
            ServicesGroup.title.label("services_group_title"),
            Service.title.label("service_title"),
            Service.instance,
            Service.id,
        )
    )
    return instances_query
