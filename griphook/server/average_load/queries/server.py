from sqlalchemy import func

from griphook.server.models import Service, Server, ServicesGroup

from griphook.server import db


def get_server_groups_services_query(server_title):
    services_query = (
        db.session.query(Server)
            .filter(Server.title == server_title)
            .join(Service)
            .join(ServicesGroup)
            .with_entities(
                Server.title.label("server_title"),
                ServicesGroup.title.label("services_group_title"),
                Service.id,
            )
    )
    return services_query


def get_server_groups_average_metric_values(joined_subquery):
    aggregated_services = (
        db.session.query(
            joined_subquery.c.services_group_title,
            joined_subquery.c.server_title,
            func.avg(joined_subquery.c.value).label("metric_average"),
        ).group_by(
            joined_subquery.c.services_group_title,
            joined_subquery.c.server_title,
        )
    )
    return aggregated_services.all()


def get_server_query(target):
    query = (
        db.session.query(Server)
            .filter(Server.title == target)
            .join(Service)
            .with_entities(
            Service.id, Server.title
        )
    )
    return query


def get_server_average_metric_value(joined_subquery):
    server_average_value = (
        db.session.query(
            joined_subquery.c.title,
            func.avg(joined_subquery.c.value).label("metric_average")
        ).group_by(joined_subquery.c.title)
    )
    return server_average_value.one()
