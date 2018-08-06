import pytest

from griphook.server.models import Server
from griphook.server.managers.exceptions import ServerManagerException
from griphook.server.managers.server_manager import ServerManager
from griphook.server.managers.constants import (
    EXC_OBJECT_DOESNT_EXISTS
)


class TestSetCPUPrice:
    def test_set_cpu_price(self, db_session, loading_test_data):
        test_server_id = 2
        test_new_cpu_price = 5.2
        ServerManager(db_session).set_cpu_price(server_id=test_server_id, new_cpu_price=test_new_cpu_price)
        server_cpu_price = db_session.query(Server.cpu_price).filter_by(id=test_server_id).scalar()
        assert server_cpu_price == test_new_cpu_price

    def test_set_cpu_price_when_server_doesnt_exists(self, db_session):
        test_server_id = 2
        test_new_cpu_price = 5.2
        with pytest.raises(ServerManagerException) as excinfo:
            ServerManager(db_session).set_cpu_price(server_id=test_server_id, new_cpu_price=test_new_cpu_price)
        assert EXC_OBJECT_DOESNT_EXISTS.format('Server', test_server_id) in str(excinfo.value)

    def test_set_cpu_price_when_price_was_set(self, db_session, loading_test_data):
        test_server_id = 1
        test_new_cpu_price = 4.2
        old_server_cpu_price = db_session.query(Server.cpu_price).filter_by(id=test_server_id).scalar()
        ServerManager(db_session).set_cpu_price(server_id=test_server_id, new_cpu_price=test_new_cpu_price)
        new_server_cpu_price = db_session.query(Server.cpu_price).filter_by(id=test_server_id).scalar()
        assert new_server_cpu_price != old_server_cpu_price
        assert new_server_cpu_price == test_new_cpu_price
