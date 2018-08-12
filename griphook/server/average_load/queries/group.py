from griphook.server.models import (
    Service,
    ServicesGroup,
)
from sqlalchemy import func

from griphook.server import db


def get_group_services_query(services_group_title):
    services_query = (
        db.session.query(ServicesGroup)
            .filter(ServicesGroup.title == services_group_title)
            .join(Service)
            .with_entities(
                ServicesGroup.title.label("services_group_title"),
                Service.title.label("service_title"),
                Service.id,
        )
    )
    return services_query


def get_services_average_metric_values(joined_subquery):
    aggregated_services = (
        db.session.query(
            joined_subquery.c.services_group_title,
            joined_subquery.c.service_title,
            func.avg(joined_subquery.c.value).label("metric_average"),
        ).group_by(
            joined_subquery.c.services_group_title,
            joined_subquery.c.service_title,
        )
    )
    return aggregated_services.all()


def get_group_query(target):
    query = (
        db.session.query(ServicesGroup)
            .filter(ServicesGroup.title == target)
            .join(Service)
            .with_entities(
            Service.id, ServicesGroup.title.label("services_group_title")
        )
    )
    return query


def get_group_average_metric_value(joined_subquery):
    service_average_value = (
        db.session.query(
            joined_subquery.c.services_group_title,
            func.avg(joined_subquery.c.value).label("metric_average")
        ).group_by(joined_subquery.c.services_group_title)
    )
    return service_average_value.one()
