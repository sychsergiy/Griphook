class ChartDataUtil(object):
    def __init__(self, root_strategy, children_strategy, **filter_params):
        self._root_strategy = root_strategy
        self._children_strategy = children_strategy
        self.filter_params = filter_params

    def get_root_metric_average_value(self):
        label, value = self._root_strategy.get_metric_average_value(**self.filter_params)
        return label, value

    def get_children_metric_average_values(self):
        data = self._children_strategy.get_items_metric_average_value(**self.filter_params)

        labels, values = self._children_strategy.convert_data_to_useful_form(data)
        # todo: here must unzip: labels, values = (*zipped)
        return labels, values
