from griphook.server.average_load.queries.common import (
    get_joined_services_batch_story_metrics_query,
    get_filtered_batch_story_query,
    get_metric_billing_query
)
# from griphook.server.average_load.strategy.service import (
#     get_service_metric_average_value_strategy,
#     get_service_instances_metric_average_values_strategy
# )
#
# from griphook.server.average_load.strategy.group import (
#     get_group_services_metric_average_values_strategy,
#     get_group_metric_average_value_strategy
# )
#
# from griphook.server.average_load.strategy.server import (
#     get_server_groups_metric_average_values_strategy,
#     get_server_metric_average_value_strategy,
# )

# from griphook.server.average_load.strategy.cluster import (
#     get_cluster_servers_metric_average_values_strategy,
#     get_cluster_metric_average_value_strategy
# )
from griphook.server.average_load.strategy.cluster import ClusterStrategy
from griphook.server.average_load.strategy.group import GroupStrategy



class ChartDataUtil(object):
    def __init__(self, target_type, **filter_params):
        """
        :param filter_params: [target, metric_type, time_from, time_until], all required
        """
        if target_type == 'service':
            pass
        #     self._get_root_chart_data = get_service_metric_average_value_strategy
        #     self._get_children_chart_data = get_service_instances_metric_average_values_strategy
        elif target_type == 'services_group':
            self._strategy = GroupStrategy(**filter_params)
        # elif target_type == "server":
        #     self._get_root_chart_data = get_server_metric_average_value_strategy
        #     self._get_children_chart_data = get_server_groups_metric_average_values_strategy
        elif target_type == 'cluster':
            self._strategy = ClusterStrategy(**filter_params)

        self.filter_params = filter_params

    def get_root_metric_average_value(self):
        joined_query = self.get_joined_services_subquery()
        label, value = self._strategy.get_root_average_metric_value(joined_query)
        return label, value

    def get_children_metric_average_values(self):
        joined_query = self.get_joined_services_subquery(False)
        query_result = self._strategy.get_children_average_metric_values(joined_query)

        chart_data = [
            (":".join(label_parts), value)
            for (*label_parts, value) in query_result
        ]
        labels, values = zip(*chart_data)
        return labels, values

    def get_joined_services_subquery(self, for_root=True):
        batch_story_subquery = get_filtered_batch_story_query(
            self.filter_params['time_from'], self.filter_params['time_until']
        ).subquery()
        metric_subquery = get_metric_billing_query(self.filter_params['metric_type']).subquery()
        if for_root:
            services_subquery = self._strategy.get_root_services_query().subquery()
        else:
            services_subquery = self._strategy.get_children_services_query().subquery()
        joined_subquery = get_joined_services_batch_story_metrics_query(
            services_subquery, batch_story_subquery, metric_subquery
        ).subquery()

        return joined_subquery
