from datetime import datetime

import pytest

from griphook.server.average_load.chart_data_util import ChartDataUtil
from griphook.server.average_load.strategy.group import GroupStrategy


@pytest.fixture(scope="function")
def filters_data():
    time_from = datetime.strptime("2018-06-10", "%Y-%m-%d")
    time_until = datetime.strptime("2018-08-10", "%Y-%m-%d")
    data = {
        "time_from": time_from,
        "time_until": time_until,
        "metric_type": "vsize",
        "target": "adv-stable",
    }
    return data


def test_get_group_services_metric_average_value(session, filters_data):
    strategy = GroupStrategy(filters_data.pop("target"))
    chart_data_util = ChartDataUtil(strategy, **filters_data)
    joined_subquery = chart_data_util.get_joined_services_subquery(False)
    instances = strategy.get_children_average_metric_values(joined_subquery)
    assert len(instances) != 0


def test_get_group_metric_average_value(session, filters_data):
    strategy = GroupStrategy(filters_data.pop("target"))
    chart_data_util = ChartDataUtil(strategy, **filters_data)
    joined_subquery = chart_data_util.get_joined_services_subquery()
    label, value = strategy.get_root_average_metric_value(joined_subquery)
    assert label == "adv-stable"
    assert value == 5845704938.62776
