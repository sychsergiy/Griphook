import pytest

from griphook.server.models import Cluster
from griphook.server.managers.exceptions import ClusterManagerException
from griphook.server.managers.cluster_manager import ClusterManager
from griphook.server.managers.constants import EXC_CLUSTER_DOESNT_EXISTS


class TestSetCPUPrice:
    def test_set_cpu_price(self, session, create_server_cluster_test_data):
        test_cluster_id = 2
        test_new_cpu_price = 5.2
        ClusterManager(session).set_cpu_price(
            cluster_id=test_cluster_id, new_cpu_price=test_new_cpu_price
        )
        cluster_cpu_price = (
            session.query(Cluster.cpu_price)
            .filter_by(id=test_cluster_id)
            .scalar()
        )
        assert cluster_cpu_price == test_new_cpu_price

    def test_set_cpu_price_when_cluster_doesnt_exists(self, session):
        test_cluster_id = 2
        test_new_cpu_price = 5.2
        with pytest.raises(ClusterManagerException) as excinfo:
            ClusterManager(session).set_cpu_price(
                cluster_id=test_cluster_id, new_cpu_price=test_new_cpu_price
            )
        assert EXC_CLUSTER_DOESNT_EXISTS.format(test_cluster_id) in str(
            excinfo.value
        )

    def test_set_cpu_price_when_price_was_set(
        self, session, create_server_cluster_test_data
    ):
        test_cluster_id = 1
        test_new_cpu_price = 4.2
        old_cluster_cpu_price = (
            session.query(Cluster.cpu_price)
            .filter_by(id=test_cluster_id)
            .scalar()
        )
        ClusterManager(session).set_cpu_price(
            cluster_id=test_cluster_id, new_cpu_price=test_new_cpu_price
        )
        new_cluster_cpu_price = (
            session.query(Cluster.cpu_price)
            .filter_by(id=test_cluster_id)
            .scalar()
        )
        assert new_cluster_cpu_price != old_cluster_cpu_price
        assert new_cluster_cpu_price == test_new_cpu_price


class TestSetMemoryPrice:
    def test_set_memory_price(
        self, session, create_server_cluster_test_data
    ):
        test_cluster_id = 2
        test_new_memory_price = 5.2
        ClusterManager(session).set_memory_price(
            cluster_id=test_cluster_id, new_memory_price=test_new_memory_price
        )
        cluster_memory_price = (
            session.query(Cluster.memory_price)
            .filter_by(id=test_cluster_id)
            .scalar()
        )
        assert cluster_memory_price == test_new_memory_price

    def test_set_memory_price_when_cluster_doesnt_exists(self, session):
        test_cluster_id = 2
        test_new_memory_price = 5.2
        with pytest.raises(ClusterManagerException) as excinfo:
            ClusterManager(session).set_memory_price(
                cluster_id=test_cluster_id,
                new_memory_price=test_new_memory_price,
            )
        assert EXC_CLUSTER_DOESNT_EXISTS.format(test_cluster_id) in str(
            excinfo.value
        )

    def test_set_memory_price_when_price_was_set(
        self, session, create_server_cluster_test_data
    ):
        test_cluster_id = 1
        test_new_memory_price = 4.2
        old_cluster_memory_price = (
            session.query(Cluster.memory_price)
            .filter_by(id=test_cluster_id)
            .scalar()
        )
        ClusterManager(session).set_memory_price(
            cluster_id=test_cluster_id, new_memory_price=test_new_memory_price
        )
        new_cluster_memory_price = (
            session.query(Cluster.memory_price)
            .filter_by(id=test_cluster_id)
            .scalar()
        )
        assert new_cluster_memory_price != old_cluster_memory_price
        assert new_cluster_memory_price == test_new_memory_price
