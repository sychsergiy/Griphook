from datetime import datetime, timedelta
import json

from flask import url_for

from griphook.server.peaks.constants import DATA_TIME_FORMAT


def test_get_clusters_hierarchy_part(app, servers,
                                     metrics, peaks_endpoint_request_data):
    client = app.test_client()
    url = url_for("peaks.peaks-api")
    server1, server2, *_ = servers
    week = 604800
    peaks_endpoint_request_data['step'] == week
    response = client.post(
        url,
        data=json.dumps(peaks_endpoint_request_data),
        follow_redirects=True,
        content_type="application/json",
    )
    assert response.status_code == 200


def request_without_reuired_field(client, url, data, field):
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
    week = 604800
    peaks_endpoint_request_data['step'] = week
    for key in peaks_endpoint_request_data:
        response = request_without_reuired_field(
            client, url, peaks_endpoint_request_data, key
        )
        error_msg = json.loads(response.data.decode("utf-8")).get("error")
        assert response.status_code == 400
        assert error_msg


def test_endpoint_response_data(app, metrics,
                                batch_storys, peaks_endpoint_request_data):
    client = app.test_client()
    time1 = batch_storys[0].time
    time2 = batch_storys[1].time
    url = url_for("peaks.peaks-api")
    week = 604800
    peaks_endpoint_request_data['step'] = week
    response = client.post(
        url,
        data=json.dumps(peaks_endpoint_request_data),
        follow_redirects=True,
        content_type="application/json",
    )
    assert response.status_code == 200
    resp_data = json.loads(response.data.decode("utf-8"))["data"]
    assert len(resp_data["timeline"]) == 2
    assert resp_data["timeline"][0] == time1.strftime(DATA_TIME_FORMAT)
    assert resp_data["timeline"][1] == time2.strftime(DATA_TIME_FORMAT)
    assert resp_data["values"][0] == 4
    assert resp_data["values"][1] == 3
    assert resp_data["metric_type"] == peaks_endpoint_request_data["metric_type"]
    peaks_endpoint_request_data["step"] = week * 4
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
    assert resp_data["timeline"][0] == time1.strftime(DATA_TIME_FORMAT)
    assert resp_data["metric_type"] == peaks_endpoint_request_data["metric_type"]