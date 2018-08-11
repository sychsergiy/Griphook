import pytest

from griphook.server.average_load.strategy.group import GroupServicesStrategy


@pytest.fixture(scope="function")
def query_result():
    return [('adv-stable', 'adv-by', 1228382856.63708), ('adv-stable', 'adv-kz', 1438634030.3411)]


def test_convert_data_to_useful_form_method(query_result):
    labels, values = GroupServicesStrategy().convert_data_to_useful_form(query_result)
    assert labels == tuple(['adv-stable:adv-by', 'adv-stable:adv-kz'])
    assert values == tuple([1228382856.63708, 1438634030.3411])

# todo: add get_items_with_average_value method test
