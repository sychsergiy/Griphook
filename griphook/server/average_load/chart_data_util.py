from griphook.server.average_load.common import (
    get_joined_services_batch_story_metrics_query,
    get_filtered_batch_story_query,
    get_metric_billing_query,
)


class ChartDataUtil(object):
    def __init__(self, strategy, **filter_params):
        """
        :param filter_params: [target, metric_type, time_from, time_until], all required
        """
        self._strategy = strategy
        self.filter_params = filter_params

    def get_root_metric_average_value(self):
        joined_query = self.get_joined_services_subquery()
        label, value = self._strategy.get_root_average_metric_value(joined_query)
        return label, value

    def get_children_metric_average_values(self):
        joined_query = self.get_joined_services_subquery(False)
        query_result = self._strategy.get_children_average_metric_values(joined_query)

        chart_data = [
            (":".join(label_parts), value) for (*label_parts, value) in query_result
        ]
        labels, values = zip(*chart_data)
        return labels, values

    def get_joined_services_subquery(self, for_root=True):
        batch_story_subquery = get_filtered_batch_story_query(
            self.filter_params["time_from"], self.filter_params["time_until"]
        ).subquery()

        metric_subquery = get_metric_billing_query(
            self.filter_params["metric_type"]
        ).subquery()

        if for_root:
            services_subquery = self._strategy.get_root_services_query().subquery()
        else:
            services_subquery = self._strategy.get_children_services_query().subquery()
        joined_subquery = get_joined_services_batch_story_metrics_query(
            services_subquery, batch_story_subquery, metric_subquery
        ).subquery()

        return joined_subquery
