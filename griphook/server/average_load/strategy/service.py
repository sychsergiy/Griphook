from sqlalchemy import func

from griphook.server import db
from griphook.server.average_load.queries.service import (
    get_services_query,
    get_batch_story_query,
    get_metric_billing_query,
    get_instances_average_metric_value,
)

from griphook.server.models import Service


def get_service_instances_metric_average_values_strategy(target, metric_type, time_from, time_until):
    instances_subquery = get_services_query(target).subquery()
    batch_story_subquery = get_batch_story_query(time_from, time_until).subquery()
    metric_subquery = get_metric_billing_query(metric_type).subquery()

    aggregated_instances = get_instances_average_metric_value(
        instances_subquery, batch_story_subquery, metric_subquery
    )
    return aggregated_instances


def get_service_metric_average_value_strategy(target, metric_type, time_from, time_until):
    batch_story_subquery = get_batch_story_query(time_from, time_until).subquery()
    metric_subquery = get_metric_billing_query(metric_type).subquery()
    query = (
        db.session.query(Service)
            .filter(Service.title == target)
            .join(metric_subquery)
            .join(batch_story_subquery)
            .with_entities(Service.title, func.avg(metric_subquery.c.value))
            .group_by(Service.title)
    )
    return query.one()
