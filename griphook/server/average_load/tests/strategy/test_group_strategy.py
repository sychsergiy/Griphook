import pytest

from datetime import datetime

from griphook.server.average_load.strategy.group import GroupServicesStrategy


@pytest.fixture(scope="function")
def query_result():
    return [
        ("adv-stable", "adv-by", 1228382856.63708),
        ("adv-stable", "adv-kz", 1438634030.3411),
    ]


def test_convert_data_to_useful_form_method(query_result):
    labels, values = GroupServicesStrategy().convert_data_to_useful_form(query_result)
    assert labels == tuple(["adv-stable:adv-by", "adv-stable:adv-kz"])
    assert values == tuple([1228382856.63708, 1438634030.3411])


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


def test_services_group_instances_query(session, filters_data):
    instances = GroupServicesStrategy().get_items_with_average_value(**filters_data)
    assert len(instances) != 0
