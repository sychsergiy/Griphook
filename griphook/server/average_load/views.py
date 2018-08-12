from datetime import datetime

from trafaret import Dict, String, DataError

from flask import jsonify, request, abort
from flask.views import MethodView

from griphook.server.average_load.chart_data_util import ChartDataUtil

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
        "children_label: List[str],
        "children_values: List[int],
    }
    """

    def post(self):
        data = request.get_json()

        error = self.is_request_data_invalid(data)
        if error:
            response = jsonify({'error': error})
            response.status_code = 400
            return response

        chart_data_util = ChartDataUtil(data.pop('target_type'), **data)
        children_data = chart_data_util.get_children_metric_average_values()
        root_label, root_value = chart_data_util.get_root_metric_average_value()
        return jsonify({})

    def is_request_data_invalid(self, data):
        try:
            template.check(data)
        except DataError as e:
            return str(e)
