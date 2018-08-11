import abc


class ChildrenStrategyAbstract(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_items_with_average_value(self, target, metric_type, time_from, time_until):
        raise NotImplementedError

    @abc.abstractmethod
    def convert_data_to_useful_form(self, query_result):
        raise NotImplementedError


class RootStrategyAbstract(object):
    pass
