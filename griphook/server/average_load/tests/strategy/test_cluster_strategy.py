import pytest

from datetime import datetime

from griphook.server.average_load.chart_data_util import ChartDataUtil
from griphook.server.average_load.strategy.cluster import (
    ClusterStrategy,
    # get_cluster_servers_metric_average_values_strategy,
    # get_cluster_metric_average_value_strategy
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
    strategy = ClusterStrategy(**filters_data)
    chart_data_util = ChartDataUtil('cluster', **filters_data)
    joined_subquery = chart_data_util.get_joined_services_subquery(False)
    instances = strategy.get_cluster_servers_average_metric_values(joined_subquery)
    print(instances)
    assert len(instances) != 0


def test_get_cluster_metric_average_value_strategy(session, filters_data):
    strategy = ClusterStrategy(**filters_data)
    chart_data_util = ChartDataUtil('cluster', **filters_data)
    joined_subquery = chart_data_util.get_joined_services_subquery()
    label, value = strategy.get_cluster_average_metric_value(joined_subquery)
    assert label == 'dev'
    assert value == 1033193632.05005
