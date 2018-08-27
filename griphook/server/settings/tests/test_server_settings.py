import json

from flask import url_for

from griphook.server.settings.constants import EXC_FIELD_IS_REQUIRED
from griphook.server.managers.constants import (
    EXC_SERVER_DOESNT_EXISTS
)


class TestGetServerSettingsAPI:
    def test_get_servers(self, client, create_server_settings_test_data):
        resp = client.get(url_for('settings_server.servers_get_all'))
        assert resp.status_code == 200
        assert len(resp.json.get('servers')) == 3


class TestServerUpdateCPUPriceSettingsAPI:
    def test_update_cpu_price(self, client, create_server_settings_test_data):
        test_server_id = 2
        test_cpu_price = 5.2
        test_data = {'id': test_server_id, 'cpu_price': test_cpu_price}
        resp = client.put(url_for('settings_server.server_update_cpu_price'), data=json.dumps(test_data))
        assert resp.status_code == 200
        assert resp.json == {'success': True}

    def test_update_cpu_price_when_server_doesnt_exists(self, client):
        test_server_id = 101
        test_cpu_price = 5.2
        test_data = {'id': test_server_id, 'cpu_price': test_cpu_price}
        resp = client.put(url_for('settings_server.server_update_cpu_price'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {'error': EXC_SERVER_DOESNT_EXISTS.format(test_server_id)}

    def test_update_cpu_price_with_wrong_parameters(self, client):
        test_server_id = 2
        test_cpu_price = 5.2
        test_data = {'id': test_server_id, 'wrong_cpu_price': test_cpu_price}
        resp = client.put(url_for('settings_server.server_update_cpu_price'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {'error': EXC_FIELD_IS_REQUIRED.format('cpu_price')}

    def test_update_cpu_price_with_not_valid_parameters(self, client):
        test_error_text = [
            {
                "loc": ["cpu_price"],
                "msg": "value is not a valid float",
                "type": "type_error.float"
            },
            {
                "loc": ["cpu_price"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer"
            }
        ]
        test_server_id = 2
        test_wrong_cpu_price = 'wrong_cpu_price_value' # should be float or int
        test_data = {'id': test_server_id, 'cpu_price': test_wrong_cpu_price}
        resp = client.put(url_for('settings_server.server_update_cpu_price'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {'error': test_error_text}


class TestServerUpdateMemoryPriceSettingsAPI:
    def test_update_memory_price(self, client, create_server_settings_test_data):
        test_server_id = 3
        test_memory_price = 2.2
        test_data = {'id': test_server_id, 'memory_price': test_memory_price}
        resp = client.put(url_for('settings_server.server_update_memory_price'), data=json.dumps(test_data))
        assert resp.status_code == 200
        assert resp.json == {'success': True}

    def test_update_memory_price_when_server_doesnt_exists(self, client):
        test_server_id = 101
        test_memory_price = 5.2
        test_data = {'id': test_server_id, 'memory_price': test_memory_price}
        resp = client.put(url_for('settings_server.server_update_memory_price'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {
            'error': EXC_SERVER_DOESNT_EXISTS.format(test_server_id)}

    def test_update_memory_price_with_wrong_parameters(self, client):
        test_server_id = 3
        test_memory_price = 5.2
        test_data = {'id': test_server_id, 'wrong_memory_price': test_memory_price}
        resp = client.put(url_for('settings_server.server_update_memory_price'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {'error': EXC_FIELD_IS_REQUIRED.format('memory_price')}

    def test_update_memory_price_with_not_valid_parameters(self, client):
        test_error_text = [
            {
                "loc": ["memory_price"],
                "msg": "value is not a valid float",
                "type": "type_error.float"
            },
            {
                "loc": ["memory_price"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer"
            }
        ]
        test_server_id = 2
        test_wrong_memory_price = 'wrong_memory_price_value'  # should be float or int
        test_data = {'id': test_server_id, 'memory_price': test_wrong_memory_price}
        resp = client.put(url_for('settings_server.server_update_memory_price'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {'error': test_error_text}
