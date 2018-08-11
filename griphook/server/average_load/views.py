from datetime import datetime

from trafaret import Dict, String, DataError

from flask import jsonify, request
from flask.views import MethodView

from .services_helper import service_average_load_query_strategy

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
        try:
            template.check(data)
        except DataError as e:
            response = jsonify({"error": str(e)})
            response.status_code = 400
            return response

        time_from = datetime.strptime(data["time_from"], "%Y-%m-%d")
        time_until = datetime.strptime(data["time_until"], "%Y-%m-%d")

        service_average_load_query_strategy(data['target'], data['metric_type'], time_from, time_until, )
        return jsonify({})
