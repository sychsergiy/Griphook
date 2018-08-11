import pytest

from griphook.server.average_load.strategy.service import ServiceInstancesStrategy


@pytest.fixture(scope="function")
def query_result():
    return [
        ('adv-stable', 'adv-by', '0', 1228382856.63708),
        ('adv-trunk', 'adv-by', '0', 1228382856.63708)
    ]


def test_convert_data_to_useful_form_method(query_result):
    labels, values = ServiceInstancesStrategy().convert_data_to_useful_form(query_result)
    assert labels == tuple(('adv-stable:adv-by:0', 'adv-trunk:adv-by:0'))
    assert values == tuple((1228382856.63708, 1228382856.63708))

# todo: add get_items_with_average_value method test
