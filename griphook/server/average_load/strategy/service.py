from griphook.server.average_load.services_helper import (
    get_services_query,
    get_batch_story_query,
    get_metric_billing_query,
    get_instances_average_metric_value
)
from griphook.server.average_load.strategy.abstract import RootStrategyAbstract, ChildrenStrategyAbstract


class ServiceInstancesStrategy(ChildrenStrategyAbstract):
    def get_items_with_average_value(
            self, target, metric_type, time_from, time_until
    ):
        instances_subquery = get_services_query(target).subquery()
        batch_story_subquery = get_batch_story_query(
            time_from, time_until
        ).subquery()
        metric_subquery = get_metric_billing_query(metric_type).subquery()

        aggregated_instances = get_instances_average_metric_value(
            instances_subquery, batch_story_subquery, metric_subquery
        )
        return aggregated_instances.all()

    def convert_data_to_useful_form(self, query_result):
        """
        :param query_result: query_children_from_target
        :return:
        """
        chart_data = [(f'{group}:{service}:{instance}', value)
                      for (group, service, instance, value) in query_result]
        labels, values = zip(*chart_data)
        return labels, values


class ServiceStrategy(RootStrategyAbstract):
    pass
