from griphook.server.models import (
    Service,
    ServicesGroup,
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
    return service_average_value.one()


def get_service_instances_query(service_title):
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


def get_service_query(target):
    query = (
        db.session.query(Service.id, Service.title.label("service_title"))
            .filter(Service.title == target)
    )
    return query
