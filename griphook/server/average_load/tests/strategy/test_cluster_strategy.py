import pytest

from griphook.server.average_load.strategy.cluster import ClusterServersStrategy


@pytest.fixture(scope="function")
def query_result():
    return [
        ('dev', 'adv', 3695958665.89072),
        ('dev', 'bart', 1658363655.43835)
    ]


def test_convert_data_to_useful_form_method(query_result):
    labels, values = ClusterServersStrategy().convert_data_to_useful_form(query_result)
    assert labels == tuple(['dev:adv', 'dev:bart'])
    assert values == tuple([3695958665.89072, 1658363655.43835])

# todo: add get_items_with_average_value method test
