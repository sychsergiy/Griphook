import pytest

from flask import url_for


@pytest.fixture
def request_data():
    request_data = {
        "metric_type": "vsize",
        "time_from": "2018-05-17",
        "time_until": "2018-08-20",
        "target_type": "all",
        "target_ids": [1],
    }
    return request_data


@pytest.mark.usefixtures("session", "client_class")
class TestGetPieChartAbsoluteDataViewTest(object):
    def test_cluster_target_type(self, request_data):
        request_data["target_type"] = "cluster"
        response = self.client.post(
            url_for("billing.get-pie-chart-absolute-data"), json=request_data
        )
        assert response.status_code == 200
        # {'labels': ['selected', 'rest'], 'values': [328252964618448.0, 320424098398567.0]}

    def test_server_target_type(self, request_data):
        request_data["target_type"] = "server"
        response = self.client.post(
            url_for("billing.get-pie-chart-absolute-data"), json=request_data
        )
        assert response.status_code == 200
        # {'labels': ['selected', 'rest'], 'values': [34566175642520.0, 614110887374490.0]}

    def test_all_target_type(self, request_data):
        request_data["target_type"] = "all"
        response = self.client.post(
            url_for("billing.get-pie-chart-absolute-data"), json=request_data
        )
        assert response.status_code == 200
        # {'labels': ['selected', 'rest'], 'values': [648677063017010.0, 0.0]}

    def test_project_target_type(self, request_data):
        request_data["target_type"] = "project"
        response = self.client.post(
            url_for("billing.get-pie-chart-absolute-data"), json=request_data
        )
        assert response.status_code == 200
        # {'labels': ['selected', 'rest'], 'values': [0, 648677063017018.0]}


@pytest.mark.usefixtures("session", "client_class")
class TestGetPieChartRelativeDataViewTest(object):
    def test_cluster_target_type(self, request_data):
        request_data["target_type"] = "cluster"
        response = self.client.post(
            url_for("billing.get-pie-chart-relative-data"), json=request_data
        )
        assert response.status_code == 200
        # print(len(response.json["values"]))

    def test_all_target_type(self, request_data):
        request_data["target_type"] = "all"
        response = self.client.post(
            url_for("billing.get-pie-chart-relative-data"), json=request_data
        )
        assert response.status_code == 200
        # print(len(response.json["values"]))

    def test_server_target_type(self, request_data):
        request_data["target_type"] = "server"
        response = self.client.post(
            url_for("billing.get-pie-chart-relative-data"), json=request_data
        )
        assert response.status_code == 200
        # print(len(response.json["values"]))

    def test_services_group_target_type(self, request_data):
        request_data["target_type"] = "services_group"
        response = self.client.post(
            url_for("billing.get-pie-chart-relative-data"), json=request_data
        )
        assert response.status_code == 200
        # print(len(response.json["values"]))
