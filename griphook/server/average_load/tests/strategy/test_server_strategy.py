import pytest

from griphook.server.average_load.strategy.group import ServicesGroupServicesStrategy


@pytest.fixture(scope="function")
def query_result():
    return [('adv', 'adv-stable', 5845704938.62776), ('adv', 'adv-trunk', 1546212393.15366)]


def test_convert_data_to_useful_form_method(query_result):
    labels, values = ServicesGroupServicesStrategy().convert_data_to_useful_form(query_result)
    assert labels == tuple(['adv:adv-stable', 'adv:adv-trunk'])
    assert values == tuple([5845704938.62776, 1546212393.15366])

# todo: add get_items_with_average_value method test
