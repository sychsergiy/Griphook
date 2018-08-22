import json

from flask import url_for


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


def test_validation_request_data(app, billing_table_endpoint_request_data):
    client = app.test_client()
    url = url_for("billing.get-filtered-billing-table-data")
    for key in billing_table_endpoint_request_data:
        response = request_without_required_field(
            client, url, billing_table_endpoint_request_data, key
        )
        error_msg = response.json
        assert response.status_code == 400
        assert error_msg


def test_billing_table_endpoint_response_data(
    app,
    clusters,
    teams,
    projects,
    servers,
    services_groups,
    services,
    billing_batch_stories,
    metrics,
    billing_table_endpoint_request_data,
):
    client = app.test_client()
    url = url_for("billing.get-filtered-billing-table-data")
    response = client.post(
        url,
        data=json.dumps(billing_table_endpoint_request_data),
        follow_redirects=True,
        content_type="application/json",
    )
    assert response.status_code == 200
    resp_data = response.json.get("table_data")
    assert len(resp_data) == 2

