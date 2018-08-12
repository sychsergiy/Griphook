import pytest

from datetime import datetime

from griphook.server.average_load.strategy.cluster import (
    get_cluster_servers_metric_average_values_strategy,
    get_cluster_metric_average_value_strategy
)


@pytest.fixture(scope="function")
def filters_data():
    time_from = datetime.strptime("2018-06-10", "%Y-%m-%d")
    time_until = datetime.strptime("2018-08-10", "%Y-%m-%d")
    data = {
        "time_from": time_from,
        "time_until": time_until,
        "metric_type": "vsize",
        "target": "dev",
    }
    return data


def test_services_group_instances_query(session, filters_data):
    instances = get_cluster_servers_metric_average_values_strategy(**filters_data)
    assert len(instances) != 0


def test_get_cluster_metric_average_value_strategy(session, filters_data):
    label, value = get_cluster_metric_average_value_strategy(**filters_data)
    assert label == 'dev'
    assert value == 1033193632.05005
