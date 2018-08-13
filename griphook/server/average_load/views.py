from flask import jsonify, request
from flask.views import MethodView

from trafaret import DataError, Dict, String

from griphook.server.average_load.chart_data_util import ChartDataUtil
from griphook.server.average_load.utils import get_strategy_for_target

WRONG_TARGET_TYPE_ERROR_MESSAGE = (
    "Wrong target type, must one of (service, services_group, server, cluster)"
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

    template = Dict(
        {
            "target": String(),
            "target_type": String(),
            "time_from": String(),
            "time_until": String(),
            "metric_type": String(),
        }
    )

    def post(self):
        request_data = request.get_json()

        error = self.is_request_data_invalid(request_data)
        if error:
            response = jsonify({"error": error})
            response.status_code = 400
            return response

        target_type = request_data.pop("target_type")
        target = request_data.pop("target")
        strategy_class = get_strategy_for_target(target_type)
        if not strategy_class:
            error_message = WRONG_TARGET_TYPE_ERROR_MESSAGE
            response = jsonify({"error": error_message})
            response.status_code = 400
            return response

        chart_data_util = ChartDataUtil(strategy_class(target), **request_data)

        target_label_value_tuple = (
            chart_data_util.get_root_metric_average_value()
        )
        if not target_label_value_tuple:
            error_message = f"Not found {target_type} with id: {target}"
            response = jsonify({"error": error_message})
            response.status_code = 404
            return response

        target_label, target_value = target_label_value_tuple

        children_labels, children_values = (
            chart_data_util.get_children_metric_average_values()
        )
        response_data = {
            "target_label": target_label,
            "target_value": target_value,
            "children_labels": children_labels,
            "children_values": children_values,
        }
        return jsonify(response_data)

    def is_request_data_invalid(self, data):
        try:
            self.template.check(data)
        except DataError as e:
            return str(e)
