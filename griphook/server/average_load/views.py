from trafaret import Dict, String, DataError

from flask import jsonify, request
from flask.views import MethodView

from griphook.server.average_load.chart_data_util import ChartDataUtil

from griphook.server.average_load.strategy.cluster import ClusterStrategy
from griphook.server.average_load.strategy.group import GroupStrategy
from griphook.server.average_load.strategy.server import ServerStrategy
from griphook.server.average_load.strategy.service import ServiceStrategy

template = Dict(
    {
        "target": String(),
        "target_type": String(),
        "time_from": String(),
        "time_until": String(),
        "metric_type": String(),
    }
)


class AverageLoadChartDataView(MethodView):
    """
    response:
    {
        "target_label": str,
        "target_value": int,
        "children_labels: List[str],
        "children_values: List[int],
    }
    """

    def post(self):
        request_data = request.get_json()

        error = self.is_request_data_invalid(request_data)
        if error:
            response = jsonify({'error': error})
            response.status_code = 400
            return response

        target_type = request_data.pop('target_type')

        if target_type == 'service':
            strategy = ServiceStrategy(**request_data)
        elif target_type == 'services_group':
            strategy = GroupStrategy(**request_data)
        elif target_type == "server":
            strategy = ServerStrategy(**request_data)
        elif target_type == 'cluster':
            strategy = ClusterStrategy(**request_data)
        else:
            raise ValueError("target_type is not valid, check request data validation function")

        chart_data_util = ChartDataUtil(strategy, **request_data)
        target_label, target_value = chart_data_util.get_root_metric_average_value()
        children_labels, children_values = chart_data_util.get_children_metric_average_values()
        response_data = {
            "target_label": target_label,
            "target_value": target_value,
            "children_labels": children_labels,
            "children_values": children_values,
        }
        return jsonify(response_data)

    def is_request_data_invalid(self, data):
        try:
            template.check(data)
        except DataError as e:
            return str(e)
