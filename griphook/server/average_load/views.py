from flask import jsonify
from flask.views import MethodView

from griphook.server.average_load.mixins import QueryParametersForMethodMixin
from griphook.server.average_load.helper import (
    ServerChartDataHelper,
    ServicesChartDataHelper,
    ServicesGroupChartDataHelper,
)


class AbstractAverageLoadAPIView(QueryParametersForMethodMixin, MethodView):
    _default_get_parameters: tuple = ('time_from', 'time_until', 'metric_type')
    get_required_parameters: tuple = tuple()

    def __init__(self, *args, **kwargs):
        self.get_required_parameters = self.get_required_parameters + self._default_get_parameters
        super(AbstractAverageLoadAPIView, self).__init__(*args, **kwargs)

    def get(self):
        raise NotImplementedError


# todo: optional argument: 'cluster'
class ServerAverageLoadView(AbstractAverageLoadAPIView):
    get_required_parameters = ('server',)

    def get(self):
        server_chart_data_helper = ServerChartDataHelper(self.parameters['server'], self.parameters['metric_type'])
        response_data = server_chart_data_helper.get_data(self.parameters['time_from'], self.parameters['time_until'])
        return jsonify(response_data)


# todo: optional arguments: 'cluster', 'server',
class ServicesGroupAverageLoadView(AbstractAverageLoadAPIView):
    get_required_parameters = ('services_group',)

    def get(self):
        sv_group_helper = ServicesGroupChartDataHelper(
            self.parameters['services_group'], self.parameters['metric_type']
        )
        response_data = sv_group_helper.get_data(
            self.parameters['time_from'], self.parameters['time_until'])
        return jsonify(response_data)


# todo: optional arguments: 'cluster', 'server', 'service_group'
class ServiceAverageLoadView(AbstractAverageLoadAPIView):
    get_required_parameters = ('service',)

    def get(self):
        services_helper = ServicesChartDataHelper(self.parameters['service'], self.parameters['metric_type'])
        response_data = services_helper.get_data(self.parameters['time_from'], self.parameters['time_until'])
        return jsonify(response_data)
