import json

from flask import url_for

from griphook.server.settings.constants import EXC_FIELD_IS_REQUIRED
from griphook.server.managers.constants import (
    EXC_CLUSTER_DOESNT_EXISTS
)


class TestGetClusterSettingsAPI:
    def test_get_clusters(self, client, create_cluster_settings_test_data):
        resp = client.get(url_for('settings.clusters_get_all'))
        assert resp.status_code == 200
        assert len(resp.json.get('clusters')) == 3


class TestClusterUpdateCPUPriceSettingsAPI:
    def test_update_cpu_price(self, client, create_cluster_settings_test_data):
        test_cluster_id = 2
        test_cpu_price = 5.2
        test_data = {'id': test_cluster_id, 'cpu_price': test_cpu_price}
        resp = client.put(url_for('settings.cluster_update_cpu_price'), data=json.dumps(test_data))
        assert resp.status_code == 200
        assert resp.json == {'success': True}

    def test_update_cpu_price_when_cluster_doesnt_exists(self, client):
        test_cluster_id = 101
        test_cpu_price = 5.2
        test_data = {'id': test_cluster_id, 'cpu_price': test_cpu_price}
        resp = client.put(url_for('settings.cluster_update_cpu_price'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {'error': EXC_CLUSTER_DOESNT_EXISTS.format(test_cluster_id)}

    def test_update_cpu_price_with_wrong_parameters(self, client):
        test_cluster_id = 2
        test_cpu_price = 5.2
        test_data = {'id': test_cluster_id, 'wrong_cpu_price': test_cpu_price}
        resp = client.put(url_for('settings.cluster_update_cpu_price'), data=json.dumps(test_data))
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
        test_cluster_id = 2
        test_wrong_cpu_price = 'wrong_cpu_price_value' # should be float or int
        test_data = {'id': test_cluster_id, 'cpu_price': test_wrong_cpu_price}
        resp = client.put(url_for('settings.cluster_update_cpu_price'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {'error': test_error_text}


class TestClusterUpdateMemoryPriceSettingsAPI:
    def test_update_memory_price(self, client, create_cluster_settings_test_data):
        test_cluster_id = 3
        test_memory_price = 2.2
        test_data = {'id': test_cluster_id, 'memory_price': test_memory_price}
        resp = client.put(url_for('settings.cluster_update_memory_price'), data=json.dumps(test_data))
        assert resp.status_code == 200
        assert resp.json == {'success': True}

    def test_update_memory_price_when_cluster_doesnt_exists(self, client):
        test_cluster_id = 101
        test_memory_price = 5.2
        test_data = {'id': test_cluster_id, 'memory_price': test_memory_price}
        resp = client.put(url_for('settings.cluster_update_memory_price'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {
            'error': EXC_CLUSTER_DOESNT_EXISTS.format(test_cluster_id)}

    def test_update_memory_price_with_wrong_parameters(self, client):
        test_cluster_id = 3
        test_memory_price = 5.2
        test_data = {'id': test_cluster_id, 'wrong_memory_price': test_memory_price}
        resp = client.put(url_for('settings.cluster_update_memory_price'), data=json.dumps(test_data))
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
        test_cluster_id = 2
        test_wrong_memory_price = 'wrong_memory_price_value'  # should be float or int
        test_data = {'id': test_cluster_id, 'memory_price': test_wrong_memory_price}
        resp = client.put(url_for('settings.cluster_update_memory_price'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {'error': test_error_text}
