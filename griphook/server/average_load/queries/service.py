from griphook.server.models import (
    Service,
    ServicesGroup,
    MetricBilling,
    BatchStoryBilling,
)
from sqlalchemy import func

from griphook.server import db


def get_instances_average_metric_values(joined_subquery):
    aggregated_instances = (
        db.session.query(
            joined_subquery.c.services_group_title,
            joined_subquery.c.service_title,
            joined_subquery.c.instance,
            func.avg(joined_subquery.c.value).label("metric_average"),
        ).group_by(
            joined_subquery.c.services_group_title,
            joined_subquery.c.service_title,
            joined_subquery.c.instance,
        )
    )
    return aggregated_instances.all()


def get_service_average_metric_value(joined_subquery):
    service_average_value = (
        db.session.query(
            joined_subquery.c.service_title,
            func.avg(joined_subquery.c.value).label("metric_average")
        ).group_by(joined_subquery.c.service_title)
    )
    return service_average_value


def get_joined_services_batch_story_metrics_query(services_subquery, batch_story_subquery, metric_subquery):
    join_query = (
        db.session.query(services_subquery, metric_subquery.c.value)
            .join(metric_subquery)
            .join(batch_story_subquery)
    )
    return join_query


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


def get_filtered_batch_story_query(time_from, time_until):
    query = (
        db.session.query(BatchStoryBilling)
            .filter(
            BatchStoryBilling.time >= time_from,
            BatchStoryBilling.time <= time_until
        ).with_entities(BatchStoryBilling.id)
    )
    return query


def get_services_with_instances_query(service_title):
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
