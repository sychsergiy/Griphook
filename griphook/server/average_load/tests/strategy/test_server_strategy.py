from datetime import datetime

import pytest

from griphook.server.average_load.strategy.server import ServerGroupsStrategy


@pytest.fixture(scope="function")
def query_result():
    return [
        ("adv", "adv-stable", 5845704938.62776),
        ("adv", "adv-trunk", 1546212393.15366),
    ]


def test_convert_data_to_useful_form_method(query_result):
    labels, values = ServerGroupsStrategy().convert_data_to_useful_form(query_result)
    assert labels == tuple(["adv:adv-stable", "adv:adv-trunk"])
    assert values == tuple([5845704938.62776, 1546212393.15366])


# todo: add get_items_with_average_value method test


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


def test_services_group_instances_query(session, filters_data):
    instances = ServerGroupsStrategy().get_items_metric_average_value(**filters_data)
    assert len(instances) != 0
