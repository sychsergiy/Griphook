import json

from flask import url_for

from griphook.server.models import Team
from griphook.server.settings.constants import EXC_FIELD_IS_REQUIRED
from griphook.server.managers.constants import (
    EXC_TEAM_ALREADY_EXISTS,
    EXC_TEAM_DOESNT_EXISTS,
)


class TestTeamCreateSettingsAPI:
    def test_create_team(self, client, db_session):
        test_title = "test_team_1"
        test_data = {"title": test_title}
        resp = client.post(
            url_for("settings_team.team-create"), data=json.dumps(test_data)
        )
        team_id = db_session.query(Team.id).filter_by(title=test_title).scalar()
        assert resp.status_code == 200
        assert resp.json == {
            "success": True,
            "id": team_id,
            "title": test_title,
        }

    def test_create_team_with_exists_title(
        self, client, create_team_settings_test_data
    ):
        test_title = "test_team_1"
        test_data = {"title": test_title}
        resp = client.post(
            url_for("settings_team.team-create"), data=json.dumps(test_data)
        )
        assert resp.status_code == 400
        assert resp.json == {
            "error": EXC_TEAM_ALREADY_EXISTS.format(test_title)
        }

    def test_create_team_with_wrong_parameters(self, client):
        test_title = "test_team_1"
        test_data = {"new_wrong_title": test_title}
        resp = client.post(
            url_for("settings_team.team-create"), data=json.dumps(test_data)
        )
        assert resp.status_code == 400
        assert resp.json == {"error": EXC_FIELD_IS_REQUIRED.format("title")}

    def test_create_team_with_not_valid_parameters(self, client):
        test_error_text = [
            {
                "loc": ["title"],
                "msg": "Length title  not valid",
                "type": "value_error",
            }
        ]
        test_title = ""  # empty title string
        test_data = {"title": test_title}
        resp = client.post(
            url_for("settings_team.team-create"), data=json.dumps(test_data)
        )
        assert resp.status_code == 400
        assert resp.json == {"error": test_error_text}


class TestTeamUpdateTitleSettingsAPI:
    def test_update_team(
        self, client, db_session, create_team_settings_test_data
    ):
        test_title = "test_new_title"
        test_team_id = 1
        test_data = {"id": test_team_id, "title": test_title}
        resp = client.put(
            url_for("settings_team.team-update-title"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 200
        assert resp.json == {"success": True}

    def test_update_team_when_it_doesnt_exists(self, client):
        test_title = "test_new_title"
        test_team_id = 101
        test_data = {"id": test_team_id, "title": test_title}
        resp = client.put(
            url_for("settings_team.team-update-title"),
            data=json.dumps(test_data),
        )

        assert resp.status_code == 400
        assert resp.json == {
            "error": EXC_TEAM_DOESNT_EXISTS.format(test_team_id)
        }

    def test_update_team_with_wrong_parameters(self, client):
        test_title = "test_new_title"
        test_team_id = 1
        test_data = {"wrong_id": test_team_id, "title": test_title}
        resp = client.put(
            url_for("settings_team.team-update-title"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 400
        assert resp.json == {"error": EXC_FIELD_IS_REQUIRED.format("id")}

    def test_update_team_with_not_valid_parameters(self, client):
        test_error_text = [
            {
                "loc": ["id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
        test_title = "test_new_title"
        test_team_id = "wrong_id_type"
        test_data = {"id": test_team_id, "title": test_title}
        resp = client.put(
            url_for("settings_team.team-update-title"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 400
        assert resp.json == {"error": test_error_text}


class TestTeamDeleteSettingsAPI:
    def test_delete_team(self, client, create_team_settings_test_data):
        test_data = {"id": 1}
        resp = client.delete(
            url_for("settings_team.team-delete"), data=json.dumps(test_data)
        )
        assert resp.status_code == 200
        assert resp.json == {"success": True}

    def test_delete_team_when_it_doesnt_exists(self, client):
        test_data = {"id": 1}
        resp = client.delete(
            url_for("settings_team.team-delete"), data=json.dumps(test_data)
        )
        assert resp.status_code == 400
        assert resp.json == {
            "error": EXC_TEAM_DOESNT_EXISTS.format(test_data.get("id"))
        }

    def test_delete_team_with_wrong_parameters(self, client):
        test_data = {"id_for_delete": 1}
        resp = client.delete(
            url_for("settings_team.team-delete"), data=json.dumps(test_data)
        )
        assert resp.status_code == 400
        assert resp.json == {"error": EXC_FIELD_IS_REQUIRED.format("id")}

    def test_delete_team_with_not_valid_parameters(self, client):
        test_error_text = [
            {
                "loc": ["id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
        test_data = {"id": "wrong_id"}
        resp = client.delete(
            url_for("settings_team.team-delete"), data=json.dumps(test_data)
        )
        assert resp.status_code == 400
        assert resp.json == {"error": test_error_text}
