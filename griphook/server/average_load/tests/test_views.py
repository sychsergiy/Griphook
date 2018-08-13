import pytest
from flask import url_for


@pytest.mark.usefixtures("client_class")
class TestAverageLoadChartDataView(object):
    def test_view_return_200_status_code(self):
        data = {
            "time_from": "2018-06-10",
            "time_until": "2018-08-10",
            "metric_type": "vsize",
            "target_type": "service",
            "target": "adv-by",
        }
        response = self.client.post(url_for("average_load.chart_data"), json=data)
        assert response.status_code == 200

    def test_view_return_400_status_code(self):
        data = {
            "time_from": "2018-06-10 0",
            "time_until": "2018-08-10 0",
            "metric_type": "vsize",
            "target": "adv-by",
        }
        response = self.client.post(url_for("average_load.chart_data"), json=data)
        assert response.status_code == 400
