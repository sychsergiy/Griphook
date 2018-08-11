from datetime import datetime

from sqlalchemy import func

from griphook.server.average_load.strategy.abstract import ChildrenStrategyAbstract
from griphook.server.models import BatchStoryBilling, MetricBilling, Service, ServicesGroup
from griphook.server import db


class GroupServicesStrategy(ChildrenStrategyAbstract):

    def get_items_with_average_value(self, time_from: datetime, time_until: datetime, target: str, metric_type: str):
        """
        :param time_from: datetime
        :param time_until: datetime
        :param target: services_group_title
        :param metric_type: vsize or user_cpu_percent
        :return: average load for each services inside current services_group
        """
        query = (
            db.session.query(ServicesGroup)
                .filter(ServicesGroup.title == target)
                .join(Service)
                .join(MetricBilling)
                .filter(MetricBilling.type == metric_type)
                .join(BatchStoryBilling)
                .filter(BatchStoryBilling.time >= time_from, BatchStoryBilling.time <= time_until)
                .with_entities(ServicesGroup.title, Service.title, func.avg(MetricBilling.value))
                .group_by(ServicesGroup.title, Service.title)
        )
        return query.all()

    def convert_data_to_useful_form(self, query_result):
        chart_data = [(f'{group}:{server}', value)
                      for (group, server, value) in query_result]
        labels, values = zip(*chart_data)
        return labels, values
