import abc


class AbstractStrategy(metaclass=abc.ABCMeta):
    def __init__(self, target, metric_type, time_from, time_until):
        self.target = target
        self.metric_type = metric_type
        self.time_from = time_from
        self.time_until = time_until

    @abc.abstractmethod
    def get_children_services_query(self):
        pass

    @abc.abstractmethod
    def get_root_services_query(self):
        pass

    @abc.abstractstaticmethod
    def get_children_average_metric_values(joined_subquery):
        pass

    @abc.abstractstaticmethod
    def get_root_average_metric_value(joined_subquery):
        pass
