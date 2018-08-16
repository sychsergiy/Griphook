import json

from flask import url_for

from griphook.server.peaks.constants import (
    RESPONSE_DATE_TIME_FORMAT,
    WEEK_TIME_STAMP,
)
from griphook.server.peaks.utils import validate_peaks_query


def test_get_clusters_hierarchy_part(
    app, servers, metrics, peaks_endpoint_request_data
):
    client = app.test_client()
    url = url_for("peaks.peaks-api")
    server1, server2, *_ = servers
    peaks_endpoint_request_data["step"] = WEEK_TIME_STAMP
    response = client.post(
        url,
        data=json.dumps(peaks_endpoint_request_data),
        follow_redirects=True,
        content_type="application/json",
    )
    assert response.status_code == 200


def request_without_required_field(client, url, data, field):
    value = data[field]
    data.pop(field)
    response = client.post(
        url,
        data=json.dumps(data),
        follow_redirects=True,
        content_type="application/json",
    )
    data[field] = value
    return response


def test_validation_request_data(app, peaks_endpoint_request_data):
    client = app.test_client()
    url = url_for("peaks.peaks-api")
    peaks_endpoint_request_data["step"] = WEEK_TIME_STAMP
    for key in peaks_endpoint_request_data:
        response = request_without_required_field(
            client, url, peaks_endpoint_request_data, key
        )
        error_msg = json.loads(response.data.decode("utf-8")).get("error")
        assert response.status_code == 400
        assert error_msg


def test_endpoint_response_data(
    app, metrics, batch_stories, peaks_endpoint_request_data
):
    client = app.test_client()
    time1 = batch_stories[0].time
    time2 = batch_stories[1].time
    url = url_for("peaks.peaks-api")
    peaks_endpoint_request_data["step"] = WEEK_TIME_STAMP
    response = client.post(
        url,
        data=json.dumps(peaks_endpoint_request_data),
        follow_redirects=True,
        content_type="application/json",
    )
    assert response.status_code == 200
    resp_data = json.loads(response.data.decode("utf-8"))["data"]
    assert len(resp_data["timeline"]) == 2
    assert resp_data["timeline"][0] == time1.strftime(RESPONSE_DATE_TIME_FORMAT)
    assert resp_data["timeline"][1] == time2.strftime(RESPONSE_DATE_TIME_FORMAT)
    assert resp_data["values"][0] == 4
    assert resp_data["values"][1] == 3
    assert (
        resp_data["metric_type"] == peaks_endpoint_request_data["metric_type"]
    )
    peaks_endpoint_request_data["step"] = WEEK_TIME_STAMP * 4
    response = client.post(
        url,
        data=json.dumps(peaks_endpoint_request_data),
        follow_redirects=True,
        content_type="application/json",
    )
    assert response.status_code == 200
    resp_data = json.loads(response.data.decode("utf-8"))["data"]
    assert len(resp_data["timeline"]) == 1
    assert resp_data["values"][0] == 4
    assert resp_data["timeline"][0] == time1.strftime(RESPONSE_DATE_TIME_FORMAT)
    assert (
        resp_data["metric_type"] == peaks_endpoint_request_data["metric_type"]
    )


def test_invalid_step_data_in_validation_function(peaks_endpoint_request_data):
    peaks_endpoint_request_data["step"] = "test"
    valid_data, error = validate_peaks_query(peaks_endpoint_request_data)
    assert error.get("error")
    assert "step" in error["error"]


def test_invalid_time_from_data_in_validation_function(
    peaks_endpoint_request_data
):
    peaks_endpoint_request_data["step"] = WEEK_TIME_STAMP
    time_from = peaks_endpoint_request_data["time_from"]
    peaks_endpoint_request_data["time_from"] = "test"
    valid_data, error = validate_peaks_query(peaks_endpoint_request_data)
    assert error.get("error")
    assert "time_from" in error["error"]
    peaks_endpoint_request_data["time_from"] = time_from


def test_invalid_time_until_data_in_validation_function(
    peaks_endpoint_request_data
):
    time_until = peaks_endpoint_request_data["time_until"]
    peaks_endpoint_request_data["time_until"] = "test"
    valid_data, error = validate_peaks_query(peaks_endpoint_request_data)
    assert error.get("error")
    assert "time_until" in error["error"]
    peaks_endpoint_request_data["time_until"] = time_until


def test_invalid_metric_type_data_in_validation_function(
    peaks_endpoint_request_data
):
    metric_type = peaks_endpoint_request_data["metric_type"]
    del peaks_endpoint_request_data["metric_type"]
    valid_data, error = validate_peaks_query(peaks_endpoint_request_data)
    assert error.get("error")
    assert "metric_type" in error["error"]
    peaks_endpoint_request_data["metric_type"] = metric_type


def test_invalid_target_type_data_in_validation_function(
    peaks_endpoint_request_data
):
    target_type = peaks_endpoint_request_data["target_type"]
    peaks_endpoint_request_data["target_type"] = "test"
    valid_data, error = validate_peaks_query(peaks_endpoint_request_data)
    assert error.get("error")
    assert "target_type" in error["error"]
    peaks_endpoint_request_data["target_type"] = target_type


def test_invalid_target_id_data_in_validation_function(
    peaks_endpoint_request_data
):
    target_id = peaks_endpoint_request_data["target_id"]
    peaks_endpoint_request_data["target_id"] = "test"
    valid_data, error = validate_peaks_query(peaks_endpoint_request_data)
    assert error.get("error")
    assert "target_id" in error["error"]
    peaks_endpoint_request_data["target_id"] = target_id
