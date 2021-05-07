from sqlalchemy import func

from griphook.server import db
from griphook.server.average_load.strategy.abstract import AbstractStrategy
from griphook.server.models import Cluster, Server, Service


class ClusterStrategy(AbstractStrategy):
    def get_children_services_query(self):
        services_query = (
            db.session.query(Cluster)
            .filter(Cluster.id == self.target_id)
            .join(Server)
            .join(Service)
            .with_entities(
                Cluster.title.label("cluster_title"),
                Server.title.label("server_title"),
                Service.id,
            )
        )
        return services_query

    @staticmethod
    def get_children_average_metric_values(joined_subquery):
        aggregated_servers = db.session.query(
            joined_subquery.c.cluster_title,
            joined_subquery.c.server_title,
            func.avg(joined_subquery.c.value).label("metric_average"),
        ).group_by(
            joined_subquery.c.cluster_title, joined_subquery.c.server_title
        )
        return aggregated_servers.all()

    def get_root_services_query(self):
        query = (
            db.session.query(Cluster)
            .filter(Cluster.id == self.target_id)
            .join(Server)
            .join(Service)
            .with_entities(Service.id, Cluster.title)
        )
        return query

    @staticmethod
    def get_root_average_metric_value(joined_subquery):
        server_average_value = db.session.query(
            joined_subquery.c.title,
            func.avg(joined_subquery.c.value).label("metric_average"),
        ).group_by(joined_subquery.c.title)
        return server_average_value.one_or_none()
