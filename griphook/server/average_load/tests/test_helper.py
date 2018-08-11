import pytest

from datetime import datetime
from griphook.server.average_load.services_helper import (
    service_average_load_query
)


@pytest.fixture(scope="function")
def request_body_data():

    # print(datetime.strftime("%Y-%m-%d"))
    time_from = datetime.strptime("2018-06-10", "%Y-%m-%d")
    time_until = datetime.strptime("2018-08-10", "%Y-%m-%d")
    print()
    data = {
        "time_from": time_from,
        "time_until": time_until,
        "metric_type": "vsize",
        "target": "adv-by",
    }
    return data


def test_service_average_load_query(session, request_body_data):
    instances = service_average_load_query(**request_body_data)

    print(instances)
    assert len(instances) != 0
