from griphook.server.models import Cluster
from griphook.server.managers.exceptions import ClusterManagerException
from griphook.server.managers.base_manager import BaseManager
from griphook.server.managers.constants import EXC_CLUSTER_DOESNT_EXISTS


class ClusterManager(BaseManager):
    def set_cpu_price(self, cluster_id: int, new_cpu_price: float) -> None:
        """
        Sets new cpu price to cluster.
        :param cluster_id: cluster id to set cpu price
        :param new_cpu_price: cpu price value
        """
        self._set_value(cluster_id, new_cpu_price, attribute_name="cpu")

    def set_memory_price(
        self, cluster_id: int, new_memory_price: float
    ) -> None:
        """
        Sets new memory price to cluster.
        :param cluster_id: cluster id to set cpu price
        :param new_memory_price: memory price value
        """
        self._set_value(cluster_id, new_memory_price, attribute_name="memory")

    def _set_value(
        self, cluster_id: int, new_value: float, attribute_name: str
    ) -> None:
        cluster = self.session.query(Cluster).filter_by(id=cluster_id).scalar()
        if not cluster:
            raise ClusterManagerException(
                EXC_CLUSTER_DOESNT_EXISTS.format(cluster_id)
            )
        if "cpu" in attribute_name:
            cluster.cpu_price = new_value
        elif "memory" in attribute_name:
            cluster.memory_price = new_value

        self.session.add(cluster)
        self.session.commit()
