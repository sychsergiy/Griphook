import pytest

from datetime import datetime

from griphook.server.average_load.strategy.service import (
    get_service_instances_metric_average_values_strategy,
    get_service_metric_average_value_strategy
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
        "target": "adv-by",
    }
    return data


def test_service_instances_average_load_query(session, filters_data):
    instances = get_service_instances_metric_average_values_strategy(**filters_data)
    assert len(instances) != 0


def test_service_average_load_query(session, filters_data):
    instance = get_service_metric_average_value_strategy(**filters_data)
    assert instance == tuple(['adv-by', 1175481906.32966])
