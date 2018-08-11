from datetime import datetime

from sqlalchemy import func

from griphook.server import db

from griphook.server.average_load.strategy.abstract import (
    RootStrategyAbstract,
    ChildrenStrategyAbstract,
)
from griphook.server.models import (
    Server,
    Service,
    ServicesGroup,
    MetricBilling,
    BatchStoryBilling,
)


class ServerGroupsStrategy(ChildrenStrategyAbstract):
    def get_items_metric_average_value(
        self, time_from: datetime, time_until: datetime, target: str, metric_type: str
    ):
        """
        :param time_from: datetime
        :param time_until: datetime
        :param target: server_title
        :param metric_type: vsize or user_cpu_percent
        :return: average load for each services inside current services_group
         (only part of service which inside current services_group)
        """
        query = (
            db.session.query(Server)
            .filter(Server.title == target)
            .join(Service)
            .join(ServicesGroup)
            .join(MetricBilling)
            .filter(MetricBilling.type == metric_type)
            .join(BatchStoryBilling)
            .filter(
                BatchStoryBilling.time >= time_from,
                BatchStoryBilling.time <= time_until,
            )
            .with_entities(
                Server.title, ServicesGroup.title, func.avg(MetricBilling.value)
            )
            .group_by(Server.title, ServicesGroup.title)
        )
        return query.all()

    def convert_data_to_useful_form(self, query_result):
        """
        :param query_result: query_children_from_target
        :return:
        """
        chart_data = [
            (f"{server}:{group}", value) for (server, group, value) in query_result
        ]
        labels, values = zip(*chart_data)
        return labels, values


class ServerStrategy(RootStrategyAbstract):
    pass
