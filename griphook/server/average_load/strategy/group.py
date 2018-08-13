from sqlalchemy import func

from griphook.server import db
from griphook.server.average_load.strategy.abstract import AbstractStrategy
from griphook.server.models import Service, ServicesGroup


class GroupStrategy(AbstractStrategy):
    def get_children_services_query(self):
        services_query = (
            db.session.query(ServicesGroup)
            .filter(ServicesGroup.title == self.target)
            .join(Service)
            .with_entities(
                ServicesGroup.title.label("services_group_title"),
                Service.title.label("service_title"),
                Service.id,
            )
        )
        return services_query

    def get_root_services_query(self):
        query = (
            db.session.query(ServicesGroup)
            .filter(ServicesGroup.title == self.target)
            .join(Service)
            .with_entities(
                Service.id, ServicesGroup.title.label("services_group_title")
            )
        )
        return query

    @staticmethod
    def get_children_average_metric_values(joined_subquery):
        aggregated_services = db.session.query(
            joined_subquery.c.services_group_title,
            joined_subquery.c.service_title,
            func.avg(joined_subquery.c.value).label("metric_average"),
        ).group_by(
            joined_subquery.c.services_group_title,
            joined_subquery.c.service_title,
        )
        return aggregated_services.all()

    @staticmethod
    def get_root_average_metric_value(joined_subquery):
        service_average_value = db.session.query(
            joined_subquery.c.services_group_title,
            func.avg(joined_subquery.c.value).label("metric_average"),
        ).group_by(joined_subquery.c.services_group_title)
        return service_average_value.one_or_none()
