from griphook.server.models import Cluster
from griphook.server.managers.exceptions import ClusterManagerException
from griphook.server.managers.base_manager import BaseManager
from griphook.server.managers.constants import EXC_CLUSTER_DOESNT_EXISTS


class ClusterManager(BaseManager):
    def set_cpu_price(self, cluster_id, new_cpu_price):
        self._set_value(cluster_id, new_cpu_price, attribute_name="cpu")

    def set_memory_price(self, cluster_id, new_memory_price):
        self._set_value(cluster_id, new_memory_price, attribute_name="memory")

    def _set_value(self, cluster_id, new_value, attribute_name):
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
