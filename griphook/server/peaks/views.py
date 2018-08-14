from flask import request, render_template, jsonify

from griphook.server.peaks.utils import (
    validate_peaks_query,
    get_peaks_query_group_by_time_step,
    peak_formatter,
)


def index():
    return render_template("peaks/index.html")


def get_peaks_for_chart():
    """
    input:
    {
        "target_type": string, | required
        "target_id": string,
        "time_from": string, | required
        "time_until": string, | required
        "metric_type": string, | required
        "step": string| required
    }

    result:
    {
        "timeline": [string],
        "value": [int],
        "metric_type": string
    }
    """
    data = request.get_json()
    if not data:
        data = request.args
    validated_data, error_data = validate_peaks_query(data)
    if error_data:
        response = jsonify(error_data)
        response.status_code = 400
    else:
        query = get_peaks_query_group_by_time_step(**validated_data)
        query_result = query.get_items()
        timeline = [peak_formatter(element) for element in query_result]
        values = [element.peaks for element in query_result]
        data = {
            "timeline": timeline,
            "values": values,
            "metric_type": query_result[0].type.value,
        }
        response_data = {"data": data}
        response = jsonify(response_data)
    return response
