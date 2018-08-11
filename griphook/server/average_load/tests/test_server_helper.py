import pytest

from datetime import datetime

from griphook.server.average_load.server_helper import server_average_load_query_strategy


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
    instances = server_average_load_query_strategy(**filters_data)
    print(instances)
    assert len(instances) != 0
