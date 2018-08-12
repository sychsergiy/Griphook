from griphook.server.average_load.strategy.service import (
    get_service_metric_average_value_strategy,
    get_service_instances_metric_average_values_strategy
)

from griphook.server.average_load.strategy.group import (
    get_group_services_metric_average_values_strategy,
    get_group_metric_average_value_strategy
)

from griphook.server.average_load.strategy.server import (
    get_server_groups_metric_average_values_strategy,
    get_server_metric_average_value_strategy,
)

from griphook.server.average_load.strategy.cluster import (
    get_cluster_servers_metric_average_values_strategy,
    get_cluster_metric_average_value_strategy
)


class ChartDataUtil(object):
    def __init__(self, target_type, **filter_params):
        """
        :param filter_params: [target, metric_type, time_from, time_until], all required
        """
        if target_type == 'service':
            self._get_root_chart_data = get_service_metric_average_value_strategy
            self._get_children_chart_data = get_service_instances_metric_average_values_strategy
        elif target_type == 'services_group':
            self._get_root_chart_data = get_group_metric_average_value_strategy
            self._get_children_chart_data = get_group_services_metric_average_values_strategy
        elif target_type == "server":
            self._get_root_chart_data = get_server_metric_average_value_strategy
            self._get_children_chart_data = get_server_groups_metric_average_values_strategy
        elif target_type == 'cluster':
            self._get_root_chart_data = get_cluster_metric_average_value_strategy
            self._get_children_chart_data = get_cluster_servers_metric_average_values_strategy

        self.filter_params = filter_params

    def get_root_metric_average_value(self):
        label, value = self._get_root_chart_data(**self.filter_params)
        return label, value

    def get_children_metric_average_values(self):
        query_result = self._get_children_chart_data(**self.filter_params)

        chart_data = [
            (":".join(label_parts), value)
            for (*label_parts, value) in query_result
        ]
        labels, values = zip(*chart_data)
        return labels, values
