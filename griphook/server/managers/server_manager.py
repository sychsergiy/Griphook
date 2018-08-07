from griphook.server.models import Server
from griphook.server.managers.exceptions import ServerManagerException
from griphook.server.managers.base_manager import BaseManager
from griphook.server.managers.constants import (
    EXC_SERVER_DOESNT_EXISTS
)


class ServerManager(BaseManager):
    def set_cpu_price(self, server_id, new_cpu_price):
        self._set_value(server_id, new_cpu_price, attribute_name='cpu')

    def set_memory_price(self, server_id, new_memory_price):
        self._set_value(server_id, new_memory_price, attribute_name='memory')

    def _set_value(self, server_id, new_value, attribute_name):
        server = self.session.query(Server).filter_by(id=server_id).scalar()
        if not server:
            raise ServerManagerException(EXC_SERVER_DOESNT_EXISTS.format(server_id))

        if 'cpu' in attribute_name:
            server.cpu_price = new_value
        elif 'memory' in attribute_name:
            server.memory_price = new_value

        self.session.add(server)
        self.session.commit()
