import json

from flask import url_for

from griphook.server.billing.constants import (
    REQUEST_DATE_TIME_FORMAT,
    RESPONSE_DATE_TIME_FORMAT,
)
from griphook.server.billing.utils.sql_utils import (
    get_services_group_metrics_chart,
    get_services_group_metrics_group_by_services,
)


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


def test_validation_request_data(client, billing_table_endpoint_request_data):
    url = url_for("billing.get_filtered_billing_table_data")
    for key in billing_table_endpoint_request_data:
        response = request_without_required_field(
            client, url, billing_table_endpoint_request_data, key
        )
        error_msg = json.loads(response.data.decode("utf-8")).get(key)
        assert response.status_code == 400
        assert error_msg


def test_billing_table_endpoint_response_data(
    client, metrics, billing_table_endpoint_request_data
):
    url = url_for("billing.get_filtered_billing_table_data")
    response = client.post(
        url,
        data=json.dumps(billing_table_endpoint_request_data),
        follow_redirects=True,
        content_type="application/json",
    )
    assert response.status_code == 200


def test_chart_api_endpoint(client, services_group_metric_request_data):
    url = url_for("billing.services-group-chart_api")
    response = client.post(
        url,
        data=json.dumps(services_group_metric_request_data),
        follow_redirects=True,
        content_type="application/json",
    )
    assert response.status_code == 200


def test_validation_request_data_chart_api_endpoint(
    client, services_group_metric_request_data
):
    services_group_metric_request_data["services_group_id"] = "1"
    services_group_metric_request_data["time_from"] = "test"
    services_group_metric_request_data["time_until"] = "test"
    url = url_for("billing.services-group-chart_api")
    response = client.post(
        url,
        data=json.dumps(services_group_metric_request_data),
        follow_redirects=True,
        content_type="application/json",
    )
    resp_data = response.json
    assert REQUEST_DATE_TIME_FORMAT in resp_data["time_from"][0]
    assert REQUEST_DATE_TIME_FORMAT in resp_data["time_until"][0]
    assert "int" in resp_data["services_group_id"][0]
    assert response.status_code == 400


def test_validation_empty_request_data_chart_api_endpoint(client):
    error_msg = "required field"
    url = url_for("billing.services-group-chart_api")
    response = client.post(
        url,
        data=json.dumps({}),
        follow_redirects=True,
        content_type="application/json",
    )
    resp_data = response.json
    assert error_msg in resp_data["time_from"][0]
    assert error_msg in resp_data["time_until"][0]
    assert error_msg in resp_data["services_group_id"][0]
    assert response.status_code == 400


def test_result_chart_data_api_endpoint(
    client, services_group_metric_request_data, billing_batch_stories, metrics
):
    url = url_for("billing.services-group-chart_api")
    response = client.post(
        url,
        data=json.dumps(services_group_metric_request_data),
        follow_redirects=True,
        content_type="application/json",
    )
    resp_data = response.json
    assert (
        billing_batch_stories[0].time.strftime(RESPONSE_DATE_TIME_FORMAT)
        in resp_data["cpu"]["timeline"]
    )
    assert metrics[0].value in resp_data["cpu"]["values"]


def test_metrics_query_grouped_by_services(
    metrics, services, billing_batch_stories, services_groups
):
    billing_batch_story_1, billing_batch_story_2, *_ = billing_batch_stories
    service_1, service_2, *_ = services
    services_group_1, services_group_2, *_ = services_groups
    service_2_result_cpu = metrics[1].value
    service_3_result_vsize = metrics[2].value + metrics[3].value
    query_result = get_services_group_metrics_group_by_services(
        services_group_id=services_group_2.id,
        time_from=billing_batch_story_1.time,
        time_until=billing_batch_story_2.time,
    )
    assert query_result[1][1] == service_3_result_vsize
    assert query_result[0][0] == service_2_result_cpu


def test_result_metrics_grouped_by_services_endpoint(
    client, services_group_metric_request_data, metrics, services_groups
):
    services_group_1, services_group_2, *_ = services_groups
    url = url_for("billing.metrics-api")
    response = client.post(
        url,
        data=json.dumps(services_group_metric_request_data),
        follow_redirects=True,
        content_type="application/json",
    )
    resp_data = response.json
    assert resp_data[0]["cpu"] == metrics[0].value
    assert resp_data[0]["memory"] == 0


def test_metric_query_by_service_group(
    billing_batch_stories, metrics, services_groups
):
    services_group_1, services_group_2, *_ = services_groups
    billing_batch_story_1, billing_batch_story_2, *_ = billing_batch_stories
    query_result = get_services_group_metrics_chart(
        services_group_id=services_group_1.id,
        time_from=billing_batch_story_1.time,
        time_until=billing_batch_story_2.time,
        metric_type=metrics[0].type,
    )
    print(query_result)
    assert query_result[0][0] == metrics[0].value
    assert query_result[0][1] == billing_batch_story_1.time
