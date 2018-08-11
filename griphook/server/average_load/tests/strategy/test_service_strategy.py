import pytest

from datetime import datetime

from griphook.server.average_load.strategy.service import ServiceInstancesStrategy, ServiceStrategy


@pytest.fixture(scope="function")
def query_result():
    return [
        ("adv-stable", "adv-by", "0", 1228382856.63708),
        ("adv-trunk", "adv-by", "0", 1228382856.63708),
    ]


def test_convert_data_to_useful_form_method(query_result):
    labels, values = ServiceInstancesStrategy().convert_data_to_useful_form(
        query_result
    )
    assert labels == tuple(("adv-stable:adv-by:0", "adv-trunk:adv-by:0"))
    assert values == tuple((1228382856.63708, 1228382856.63708))


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
    instances = ServiceInstancesStrategy().get_items_metric_average_value(**filters_data)
    assert len(instances) != 0


def test_service_average_load_query(session, filters_data):
    instance = ServiceStrategy().get_metric_average_value(**filters_data)
    assert instance == tuple(['adv-by', 1175481906.32966])
