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
        "target": "adv-by",
    }

    return data


@pytest.mark.usefixtures("client_class")
class TestAverageLoadChartDataView(object):
    def test_view_return_200_status_code(self, request_data):
        response = self.client.post(
            url_for("average_load.chart_data"), json=request_data
        )
        assert response.status_code == 200

    def test_400_status_code_when_request_data_not_enough_arguments(
        self, request_data
    ):
        request_data.pop("metric_type", None)

        response = self.client.post(
            url_for("average_load.chart_data"), json=request_data
        )
        assert response.status_code == 400
        assert (
            response.get_json()["error"]
            == "{'metric_type': DataError(is required)}"
        )

    def test_wrong_target_type(self, request_data):
        request_data["target_type"] = "wrong"
        response = self.client.post(
            url_for("average_load.chart_data"), json=request_data
        )
        assert response.status_code == 400
        assert response.get_json()["error"] == WRONG_TARGET_TYPE_ERROR_MESSAGE

    def test_correct_target_type(self, request_data):
        request_data["target_type"] = "service"
        request_data["target"] = "adv-by"

        response = self.client.post(
            url_for("average_load.chart_data"), json=request_data
        )
        assert response.status_code == 200

    def test_404_status_code_when_target_not_founded(self, request_data):
        request_data["target_type"] = "service"
        request_data["target"] = "wrong"
        response = self.client.post(
            url_for("average_load.chart_data"), json=request_data
        )
        assert response.status_code == 404
        error_message = "Not found service with id: wrong"
        assert response.get_json()["error"] == error_message
