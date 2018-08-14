import pytest

from flask import url_for

from griphook.server.average_load.views import WRONG_TARGET_TYPE_ERROR_MESSAGE


@pytest.fixture(scope="function")
def request_data():
    """request data template for average load endpoint"""
    data = {
        "time_from": "2018-06-10",
        "time_until": "2018-08-10",
        "metric_type": "vsize",
        "target_type": "service",
        "target_id": 1,
    }

    return data


@pytest.mark.usefixtures("client_class")
class TestAverageLoadChartDataView(object):
    def test_view_return_200_status_code(self, request_data):
        response = self.client.post(
            url_for("average_load.chart_data"), json=request_data
        )
        assert response.status_code == 200

    def test_400_status_code_when_not_enough_request_arguments(
        self, request_data
    ):
        request_data.pop("metric_type")
        response = self.client.post(
            url_for("average_load.chart_data"), json=request_data
        )
        assert response.status_code == 400

        expected_message = "{'metric_type': DataError(is required)}"
        response_message = response.get_json()["error"]
        assert response_message == expected_message

    def test_wrong_target_type(self, request_data):
        request_data["target_type"] = "wrong"
        response = self.client.post(
            url_for("average_load.chart_data"), json=request_data
        )
        assert response.status_code == 400
        assert response.get_json()["error"] == WRONG_TARGET_TYPE_ERROR_MESSAGE

    def test_correct_target_type(self, request_data):
        request_data["target_type"] = "service"
        request_data["target_id"] = 1

        response = self.client.post(
            url_for("average_load.chart_data"), json=request_data
        )
        assert response.status_code == 200

    def test_404_status_code_when_target_not_founded(self, request_data):
        request_data["target_type"] = "service"
        request_data["target_id"] = 10000
        response = self.client.post(
            url_for("average_load.chart_data"), json=request_data
        )

        expected_response_data = {
            "target_label": "",
            "target_value": "",
            "children_labels": [],
            "children_values": [],
            "metric_type": request_data["metric_type"],
        }

        assert response.status_code == 200
        assert response.get_json() == expected_response_data
