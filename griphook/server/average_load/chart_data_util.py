from griphook.server.average_load.queries import (
    get_joined_services_batch_story_metrics_query,
    get_filtered_batch_story_query,
    get_metric_billing_query,
)


class ChartDataUtil(object):
    def __init__(self, strategy, metric_type, time_from, time_until):
        self._strategy = strategy
        self.metric_type = metric_type
        self.time_from = time_from
        self.time_until = time_until

    def get_root_metric_average_value(self):
        joined_query = self.get_joined_services_subquery()
        label_value_tuple = self._strategy.get_root_average_metric_value(joined_query)
        return label_value_tuple

    def get_children_metric_average_values(self):
        joined_query = self.get_joined_services_subquery(for_root=False)
        query_result = self._strategy.get_children_average_metric_values(joined_query)

        chart_data = [
            (":".join(label_parts), value) for (*label_parts, value) in query_result
        ]
        labels, values = zip(*chart_data)
        return labels, values

    def get_joined_services_subquery(self, for_root=True):
        batch_story_subquery = get_filtered_batch_story_query(
            self.time_from, self.time_until
        ).subquery()

        metric_subquery = get_metric_billing_query(self.metric_type).subquery()

        if for_root:
            services_subquery = self._strategy.get_root_services_query().subquery()
        else:
            services_subquery = self._strategy.get_children_services_query().subquery()
        joined_subquery = get_joined_services_batch_story_metrics_query(
            services_subquery, batch_story_subquery, metric_subquery
        ).subquery()

        return joined_subquery
