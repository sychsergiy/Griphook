import json

from flask import url_for

from griphook.server.models import Project


class TestProjectSettingsAPI:
    def test_create_project(self, client, db_session):
        test_title = 'test_project_1'
        test_data = {'title': test_title}
        res = client.post(url_for('settings.project'), data=json.dumps(test_data))

        project_id = db_session.query(Project.id).filter_by(title=test_title).scalar()

        assert res.status_code == 200
        assert res.json == {'id': project_id, 'title': test_title}

    def test_create_project_with_exists_title(self, client, create_project_settings_test_data):
        test_title = 'test_project_1'
        test_data = {'title': test_title}
        res = client.post(url_for('settings.project'), data=json.dumps(test_data))
        assert res.status_code == 400

    def test_update_project(self, client, db_session, create_project_settings_test_data):
        test_title = 'test_new_title'
        test_project_id = 1

        test_data = {'id': test_project_id, 'title': test_title}
        res = client.put(url_for('settings.project'), data=json.dumps(test_data))

        new_project_title = db_session.query(Project.title).filter_by(id=test_project_id).scalar()

        assert res.status_code == 200
        assert new_project_title == test_title

    def test_update_project_when_it_doesnt_exists(self, client):
        test_title = 'test_new_title'
        test_project_id = 101

        test_data = {'id': test_project_id, 'title': test_title}
        res = client.put(url_for('settings.project'), data=json.dumps(test_data))

        assert res.status_code == 400

    def test_delete_project(self, client, create_project_settings_test_data):
        test_data = {'id': 1}
        res = client.delete(url_for('settings.project'), data=json.dumps(test_data))
        assert res.status_code == 200

    def test_delete_project_when_it_doesnt_exists(self, client):
        test_data = {'id': 1}
        res = client.delete(url_for('settings.project'), data=json.dumps(test_data))
        assert res.status_code == 400
