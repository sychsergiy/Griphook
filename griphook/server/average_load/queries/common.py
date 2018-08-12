from griphook.server import db

from griphook.server.models import MetricBilling, BatchStoryBilling


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


# todo: rename this function
def average_load_query_builder(
        target, metric_type, time_from, time_until, services_query_getter, average_metric_value_getter
):
    batch_story_subquery = get_filtered_batch_story_query(time_from, time_until).subquery()
    metric_subquery = get_metric_billing_query(metric_type).subquery()
    services_subquery = services_query_getter(target).subquery()
    joined_subquery = get_joined_services_batch_story_metrics_query(
        services_subquery, batch_story_subquery, metric_subquery
    ).subquery()

    return average_metric_value_getter(joined_subquery)
