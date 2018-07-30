from flask import jsonify
from flask.views import MethodView

from griphook.server.average_load.graphite import (
    get_average_service_load_chart_data,
    get_average_services_group_load_chart_data,
    get_average_server_load_chart_data
)
from griphook.server.models import ServicesGroup, Service
from griphook.server.average_load.mixins import QueryParametersForMethodMixin


# todo: how graphite handle so many instances in query_params,
#  check if it is possible to send only server or services_group


class AbstractAverageLoadAPIView(QueryParametersForMethodMixin, MethodView):
    _default_get_parameters: tuple = ('time_from', 'time_until', 'metric_type')
    get_required_parameters: tuple = tuple()

    def __init__(self, *args, **kwargs):
        self.get_required_parameters = self.get_required_parameters + self._default_get_parameters
        super(AbstractAverageLoadAPIView, self).__init__(*args, **kwargs)

    def services_query(self, **kwargs):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError


class ServerAverageLoadView(AbstractAverageLoadAPIView):
    get_required_parameters = ('server',)

    def get(self):
        target_services = [':'.join(target) for target in self.services_query(self.parameters['server'])]
        response_data = get_average_server_load_chart_data(self.parameters['server'], target_services,
                                                           self.parameters['time_from'], self.parameters['time_until'])

        response = jsonify(response_data)
        return response

    def services_query(self, server_title: str) -> list:
        return (
            Service.query
                .filter(Service.server == server_title)
                .join(ServicesGroup)
                .with_entities(Service.server, ServicesGroup.title, Service.title, Service.instance)
        ).all()


class ServicesGroupAverageLoadView(AbstractAverageLoadAPIView):
    get_required_parameters = ('services_group',)

    def get(self):
        target_services = [':'.join(target) for target in self.services_query(self.parameters['services_group'])]
        response_data = get_average_services_group_load_chart_data(
            self.parameters['services_group'], target_services,
            self.parameters['time_from'], self.parameters['time_until']
        )
        return jsonify(response_data)

    def services_query(self, service_group_title: str) -> list:
        return (
            ServicesGroup.query
                .filter(ServicesGroup.title == service_group_title)
                .join(Service)
                .with_entities(Service.server, ServicesGroup.title, Service.title, Service.instance)
        ).all()


class ServiceAverageLoadView(AbstractAverageLoadAPIView):
    get_required_parameters = ('service',)

    def get(self):
        target_services = [':'.join(target) for target in self.services_query(self.parameters['service'])]
        response_data = get_average_service_load_chart_data(
            self.parameters['service'], target_services,
            self.parameters['time_from'], self.parameters['time_until']
        )
        return jsonify(response_data)

    def services_query(self, service):
        return (
            Service.query
                .filter(Service.title == service)
                .join(ServicesGroup)
                .with_entities(Service.server, ServicesGroup.title, Service.title, Service.instance)
        ).all()

# todo: use summarize to get average for every instance,
# todo: than use averageSeries graphite function to find total average

# todo: change arguemtns (server_title, service_group_title, ...) to (server, services_group, ...) in filters blueprint
