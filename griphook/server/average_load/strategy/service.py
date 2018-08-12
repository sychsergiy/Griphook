from griphook.server import db
from griphook.server.average_load.queries.service import (
    get_services_with_instances_query,
    get_filtered_batch_story_query,
    get_metric_billing_query,
    get_instances_average_metric_values,
    get_joined_services_batch_story_metrics_query,
    get_service_average_metric_value
)

from griphook.server.models import Service


def get_service_instances_metric_average_values_strategy(target, metric_type, time_from, time_until):
    instances_subquery = get_services_with_instances_query(target).subquery()
    batch_story_subquery = get_filtered_batch_story_query(time_from, time_until).subquery()
    metric_subquery = get_metric_billing_query(metric_type).subquery()

    joined_subquery = get_joined_services_batch_story_metrics_query(
        instances_subquery, batch_story_subquery, metric_subquery
    ).subquery()

    aggregated_instances = get_instances_average_metric_values(joined_subquery)
    return aggregated_instances


def get_service_metric_average_value_strategy(target, metric_type, time_from, time_until):
    batch_story_subquery = get_filtered_batch_story_query(time_from, time_until).subquery()
    metric_subquery = get_metric_billing_query(metric_type).subquery()

    services_subquery = db.session.query(Service.id, Service.title.label("service_title")).filter(
        Service.title == target).subquery()

    joined_subquery = get_joined_services_batch_story_metrics_query(
        services_subquery, batch_story_subquery, metric_subquery
    ).subquery()

    result_query = get_service_average_metric_value(joined_subquery)
    return result_query.one()
