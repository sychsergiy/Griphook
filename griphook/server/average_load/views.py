from flask import jsonify
from flask.views import MethodView

from griphook.server.average_load.mixins import QueryParametersForMethodMixin
from griphook.server.average_load.helper import (
    ServerChartDataHelper,
    ServicesChartDataHelper,
    ServicesGroupChartDataHelper,
)


# todo: optional argument: 'cluster'
class ServerAverageLoadView(QueryParametersForMethodMixin, MethodView):
    """
    Endpoint with data for server average load chart
    returns average load for server and for every service_group inside current server
    in following format:
    {
        "root": {
            "target": "values"
            "value": "value"
            }
        "children": [
            {"target": "value", "value": "value"},
            ...
        ]
    }
    """

    get_required_parameters = ("time_from", "time_until", "metric_type", "server")

    def get(self):
        server_chart_data_helper = ServerChartDataHelper(
            self.parameters["server"], self.parameters["metric_type"]
        )
        response_data = server_chart_data_helper.get_data(
            self.parameters["time_from"], self.parameters["time_until"]
        )
        return jsonify(response_data)


# todo: optional arguments: 'cluster', 'server',
class ServicesGroupAverageLoadView(QueryParametersForMethodMixin, MethodView):
    """
    Endpoint with data for service_group average load chart
    returns average load for server and for every service inside current service_group
    in following format:
    {
        "root": {
            "target": "values"
            "value": "value"
            }
        "children": [
            {"target": "value", "value": "value"},
            ...
        ]
    }
    """

    get_required_parameters = (
        "time_from",
        "time_until",
        "metric_type",
        "services_group",
    )

    def get(self):
        sv_group_helper = ServicesGroupChartDataHelper(
            self.parameters["services_group"], self.parameters["metric_type"]
        )
        response_data = sv_group_helper.get_data(
            self.parameters["time_from"], self.parameters["time_until"]
        )
        return jsonify(response_data)


# todo: optional arguments: 'cluster', 'server', 'service_group'
class ServiceAverageLoadView(QueryParametersForMethodMixin, MethodView):
    """
    Endpoint with data for service average load chart
    returns average load for server and for every instance inside current service
    in following format:
    {
        "root": {
            "target": "values"
            "value": "value"
            }
        "children": [
            {"target": "value", "value": "value"},
            ...
        ]
    }
    """

    get_required_parameters = ("time_from", "time_until", "metric_type", "service")

    def get(self):
        services_helper = ServicesChartDataHelper(
            self.parameters["service"], self.parameters["metric_type"]
        )
        response_data = services_helper.get_data(
            self.parameters["time_from"], self.parameters["time_until"]
        )
        return jsonify(response_data)


# todo: maybe separate endpoints for getting average_load data for root and children
