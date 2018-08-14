import abc


class AbstractStrategy(metaclass=abc.ABCMeta):
    def __init__(self, target_id):
        self.target_id = target_id

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
