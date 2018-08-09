import json

from flask import current_app, request, render_template

from griphook.server.peaks.utils import validate_peaks_query, peaks_query, peak_formatter


def index():
    return render_template('peaks/index.html')


def get_peaks():
    data = request.get_json()
    validated_data, error_data = validate_peaks_query(data)
    if error_data:
        response = current_app.response_class(
            response=json.dumps(error_data),
            status=400,
            mimetype='application/json'
        )
    else:
        query = peaks_query(validated_data)
        query_result = query.all()
        timeline = [peak_formatter(element) for element in query_result]
        values = [element.peaks for element in query_result]
        data = {"timeline": timeline, "values": values, 'metric_type': query_result[0].type.value}
        response_data = {'data': data}
        response = current_app.response_class(
            response=json.dumps(response_data),
            status=200,
            mimetype='application/json'
        )
    return response
