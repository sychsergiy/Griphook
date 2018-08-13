from sqlalchemy import func

from griphook.server import db
from griphook.server.average_load.strategy.abstract import AbstractStrategy
from griphook.server.models import Service, ServicesGroup


class ServiceStrategy(AbstractStrategy):
    def get_children_services_query(self):
        """
        instances are children for service
        """
        instances_query = (
            db.session.query(Service)
            .filter(Service.title == self.target)
            .join(ServicesGroup)
            .with_entities(
                ServicesGroup.title.label("services_group_title"),
                Service.title.label("service_title"),
                Service.instance,
                Service.id,
            )
        )
        return instances_query

    @staticmethod
    def get_children_average_metric_values(joined_subquery):
        aggregated_instances = db.session.query(
            joined_subquery.c.services_group_title,
            joined_subquery.c.service_title,
            joined_subquery.c.instance,
            func.avg(joined_subquery.c.value).label("metric_average"),
        ).group_by(
            joined_subquery.c.services_group_title,
            joined_subquery.c.service_title,
            joined_subquery.c.instance,
        )
        return aggregated_instances.all()

    def get_root_services_query(self):
        query = db.session.query(
            Service.id, Service.title.label("service_title")
        ).filter(Service.title == self.target)
        return query

    @staticmethod
    def get_root_average_metric_value(joined_subquery):
        service_average_value = db.session.query(
            joined_subquery.c.service_title,
            func.avg(joined_subquery.c.value).label("metric_average"),
        ).group_by(joined_subquery.c.service_title)
        return service_average_value.one_or_none()
