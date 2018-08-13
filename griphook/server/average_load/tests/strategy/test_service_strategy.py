from datetime import datetime

import pytest

from griphook.server.average_load.chart_data_util import ChartDataUtil
from griphook.server.average_load.strategy.service import ServiceStrategy


@pytest.fixture(scope="function")
def filters_data():
    time_from = datetime.strptime("2018-06-10", "%Y-%m-%d")
    time_until = datetime.strptime("2018-08-10", "%Y-%m-%d")
    data = {
        "time_from": time_from,
        "time_until": time_until,
        "metric_type": "vsize",
        "target": "adv-by",
    }
    return data


def test_get_service_instances_metric_average_values(session, filters_data):
    strategy = ServiceStrategy(filters_data.pop('target'))
    chart_data_util = ChartDataUtil(strategy, **filters_data)
    joined_subquery = chart_data_util.get_joined_services_subquery(False)
    instances = strategy.get_children_average_metric_values(joined_subquery)
    assert len(instances) != 0


def test_get_service_metric_average_value(session, filters_data):
    strategy = ServiceStrategy(filters_data.pop('target'))
    chart_data_util = ChartDataUtil(strategy, **filters_data)
    joined_subquery = chart_data_util.get_joined_services_subquery()
    label, value = strategy.get_root_average_metric_value(joined_subquery)
    assert label, value == ("adv-by", 1175481906.32966)
