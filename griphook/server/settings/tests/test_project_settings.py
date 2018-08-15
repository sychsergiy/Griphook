import json

from flask import url_for

from griphook.server.models import Project
from griphook.server.settings.constants import EXC_FIELD_IS_REQUIRED
from griphook.server.managers.constants import (
    EXC_PROJECT_ALREADY_EXISTS,
    EXC_PROJECT_DOESNT_EXISTS
)


class TestProjectCreateSettingsAPI:
    def test_create_project(self, client, db_session):
        test_title = 'test_project_1'
        test_data = {'title': test_title}
        resp = client.post(url_for('settings.project_create'), data=json.dumps(test_data))
        project_id = db_session.query(Project.id).filter_by(title=test_title).scalar()
        assert resp.status_code == 200
        assert resp.json == {'success': True, 'id': project_id, 'title': test_title}

    def test_create_project_with_exists_title(self, client, create_project_settings_test_data):
        test_title = 'test_project_1'
        test_data = {'title': test_title}
        resp = client.post(url_for('settings.project_create'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {'error': EXC_PROJECT_ALREADY_EXISTS.format(test_title)}

    def test_create_project_with_wrong_parameters(self, client):
        test_title = 'test_project_1'
        test_data = {'new_wrong_title': test_title}
        resp = client.post(url_for('settings.project_create'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {'error': EXC_FIELD_IS_REQUIRED.format('title')}

    def test_create_project_with_not_valid_parameters(self, client):
        test_error_text = [
            {
                "loc": ["title"],
                "msg": "Length title  not valid",
                "type": "value_error"
            }
        ]
        test_title = ''  # empty title string
        test_data = {'title': test_title}
        resp = client.post(url_for('settings.project_create'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {'error': test_error_text}


class TestProjectUpdateTitleSettingsAPI:
    def test_update_project(self, client, db_session, create_project_settings_test_data):
        test_title = 'test_new_title'
        test_project_id = 1
        test_data = {'id': test_project_id, 'title': test_title}
        resp = client.put(url_for('settings.project_update_title'), data=json.dumps(test_data))
        assert resp.status_code == 200
        assert resp.json == {'success': True}

    def test_update_project_when_it_doesnt_exists(self, client):
        test_title = 'test_new_title'
        test_project_id = 101
        test_data = {'id': test_project_id, 'title': test_title}
        resp = client.put(url_for('settings.project_update_title'), data=json.dumps(test_data))

        assert resp.status_code == 400
        assert resp.json == {'error': EXC_PROJECT_DOESNT_EXISTS.format(test_project_id)}

    def test_update_project_with_wrong_parameters(self, client):
        test_title = 'test_new_title'
        test_project_id = 1
        test_data = {'wrong_id': test_project_id, 'title': test_title}
        resp = client.put(url_for('settings.project_update_title'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {'error': EXC_FIELD_IS_REQUIRED.format('id')}

    def test_update_project_with_not_valid_parameters(self, client):
        test_error_text = [
            {
                "loc": ["id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer"
            }
        ]
        test_title = 'test_new_title'
        test_project_id = "wrong_id_type"
        test_data = {'id': test_project_id, 'title': test_title}
        resp = client.put(url_for('settings.project_update_title'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {'error': test_error_text}


class TestProjectDeleteSettingsAPI:
    def test_delete_project(self, client, create_project_settings_test_data):
        test_data = {'id': 1}
        resp = client.delete(url_for('settings.project_delete'), data=json.dumps(test_data))
        assert resp.status_code == 200
        assert resp.json == {'success': True}

    def test_delete_project_when_it_doesnt_exists(self, client):
        test_data = {'id': 1}
        resp = client.delete(url_for('settings.project_delete'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {'error': EXC_PROJECT_DOESNT_EXISTS.format(test_data.get('id'))}

    def test_delete_project_with_wrong_parameters(self, client):
        test_data = {'id_for_delete': 1}
        resp = client.delete(url_for('settings.project_delete'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {'error': EXC_FIELD_IS_REQUIRED.format('id')}

    def test_delete_project_with_not_valid_parameters(self, client):
        test_error_text = [
            {
                "loc": ["id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer"
            }
        ]
        test_data = {'id': "wrong_id"}
        resp = client.delete(url_for('settings.project_delete'), data=json.dumps(test_data))
        assert resp.status_code == 400
        assert resp.json == {'error': test_error_text}
