from datetime import datetime

import pytest

from griphook.server.average_load.strategy.server import (
    get_server_groups_metric_average_values_strategy,
    get_server_metric_average_value_strategy
)


@pytest.fixture(scope="function")
def filters_data():
    time_from = datetime.strptime("2018-06-10", "%Y-%m-%d")
    time_until = datetime.strptime("2018-08-10", "%Y-%m-%d")
    data = {
        "time_from": time_from,
        "time_until": time_until,
        "metric_type": "vsize",
        "target": "adv",
    }
    return data


def test_get_server_groups_metric_average_values_strategy(session, filters_data):
    groups_chart_data_sequence = get_server_groups_metric_average_values_strategy(**filters_data)
    assert len(groups_chart_data_sequence) != 0


def test_get_server_metric_average_value_strategy(session, filters_data):
    label, value = get_server_metric_average_value_strategy(**filters_data)
    assert label == 'adv'
    assert value == 3695958665.89072
