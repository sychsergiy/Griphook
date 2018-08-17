from sqlalchemy import func

from griphook.server import db
from griphook.server.average_load.strategy.abstract import AbstractStrategy
from griphook.server.models import Server, Service, ServicesGroup


class ServerStrategy(AbstractStrategy):
    def get_children_services_query(self):
        """
        services groups are children of server,
         but one services group can be distributes between few servers,
         take only part from current server
         """
        services_query = (
            db.session.query(Server)
            .filter(Server.id == self.target_id)
            .join(Service)
            .join(ServicesGroup)
            .with_entities(
                Server.title.label("server_title"),
                ServicesGroup.title.label("services_group_title"),
                Service.id,
            )
        )
        return services_query

    @staticmethod
    def get_children_average_metric_values(joined_subquery):
        aggregated_services = db.session.query(
            joined_subquery.c.services_group_title,
            joined_subquery.c.server_title,
            func.avg(joined_subquery.c.value).label("metric_average"),
        ).group_by(
            joined_subquery.c.services_group_title,
            joined_subquery.c.server_title,
        )
        return aggregated_services.all()

    def get_root_services_query(self):
        query = (
            db.session.query(Server)
            .filter(Server.id == self.target_id)
            .join(Service)
            .with_entities(Service.id, Server.title)
        )
        return query

    @staticmethod
    def get_root_average_metric_value(joined_subquery):
        server_average_value = db.session.query(
            joined_subquery.c.title,
            func.avg(joined_subquery.c.value).label("metric_average"),
        ).group_by(joined_subquery.c.title)
        return server_average_value.one_or_none()
