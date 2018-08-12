import pytest

from datetime import datetime

from griphook.server.average_load.strategy.group import (
    get_group_metric_average_value_strategy,
    get_group_services_metric_average_values_strategy
)


# todo: add get_items_with_average_value method test


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


def test_get_group_services_metric_average_value_strategy(session, filters_data):
    instances = get_group_services_metric_average_values_strategy(**filters_data)
    assert len(instances) != 0


def test_get_group_metric_average_value_strategy(session, filters_data):
    label, value = get_group_metric_average_value_strategy(**filters_data)
    assert label == 'adv-stable'
    assert value == 5845704938.62776
