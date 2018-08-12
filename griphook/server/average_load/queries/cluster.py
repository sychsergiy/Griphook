from sqlalchemy import func

from griphook.server.models import Service, Server, Cluster

from griphook.server import db


def get_cluster_server_services_query(cluster_title):
    services_query = (
        db.session.query(Cluster)
            .filter(Cluster.title == cluster_title)
            .join(Server)
            .join(Service)
            .with_entities(
            Cluster.title.label("cluster_title"),
            Server.title.label("server_title"),
            Service.id,
        )
    )
    return services_query


def get_cluster_servers_average_metric_values(joined_subquery):
    aggregated_servers = (
        db.session.query(
            joined_subquery.c.cluster_title,
            joined_subquery.c.server_title,
            func.avg(joined_subquery.c.value).label("metric_average"),
        ).group_by(
            joined_subquery.c.cluster_title,
            joined_subquery.c.server_title,
        )
    )
    return aggregated_servers.all()


def get_cluster_query(target):
    query = (
        db.session.query(Cluster)
            .filter(Cluster.title == target)
            .join(Server)
            .join(Service)
            .with_entities(Service.id, Cluster.title)
    )
    return query


def get_cluster_average_metric_value(joined_subquery):
    server_average_value = (
        db.session.query(
            joined_subquery.c.title,
            func.avg(joined_subquery.c.value).label("metric_average")
        ).group_by(joined_subquery.c.title)
    )
    return server_average_value.one()
