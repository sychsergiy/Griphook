from flask import jsonify
from flask.views import MethodView

from griphook.server.average_load.servers import get_server_load_chart_data
from griphook.server.average_load.sv_groups import get_average_services_group_load_chart_data

from griphook.server.models import ServicesGroup, Service
from griphook.server.average_load.mixins import QueryParametersForMethodMixin


class AbstractAverageLoadAPIView(QueryParametersForMethodMixin, MethodView):
    _default_get_parameters: tuple = ('time_from', 'time_until', 'metric_type')
    get_required_parameters: tuple = tuple()

    def __init__(self, *args, **kwargs):
        self.get_required_parameters = self.get_required_parameters + self._default_get_parameters
        super(AbstractAverageLoadAPIView, self).__init__(*args, **kwargs)

    def get(self):
        raise NotImplementedError


class ServerAverageLoadView(AbstractAverageLoadAPIView):
    get_required_parameters = ('server',)

    def get(self):
        response_data = get_server_load_chart_data(
            self.parameters['server'], self.parameters['time_from'],
            self.parameters['time_until'], self.parameters['metric_type'])
        return jsonify(response_data)


class ServicesGroupAverageLoadView(AbstractAverageLoadAPIView):
    get_required_parameters = ('services_group',)

    def get(self):
        response_data = get_average_services_group_load_chart_data(
            self.parameters['services_group'], self.parameters['time_from'],
            self.parameters['time_until'], self.parameters['metric_type'])
        return jsonify(response_data)


class ServiceAverageLoadView(AbstractAverageLoadAPIView):
    get_required_parameters = ('service',)

    def get(self):
        return jsonify({})

    # def get(self):
    #     target_services = [':'.join(target) for target in self.services_query(self.parameters['service'])]
    #     response_data = get_average_service_load_chart_data(
    #         self.parameters['service'], target_services,
    #         self.parameters['time_from'], self.parameters['time_until']
    #     )
    #     return jsonify(response_data)

    def services_query(self, service):
        return (
            Service.query
                .filter(Service.title == service)
                .join(ServicesGroup)
                .with_entities(Service.server, ServicesGroup.title, Service.title, Service.instance)
        ).all()
# todo: average_load_server_view already working, code the same for service_groups and services

# todo: change arguments (server_title, service_group_title, ...) to (server, services_group, ...) in filters blueprint
