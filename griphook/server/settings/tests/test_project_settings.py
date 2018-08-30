import json

from flask import url_for

from griphook.server.models import Project
from griphook.server.settings.constants import EXC_FIELD_IS_REQUIRED
from griphook.server.managers.constants import (
    EXC_SERVICES_GROUP_DOESNT_EXISTS,
    EXC_PROJECT_ALREADY_EXISTS,
    EXC_PROJECT_DOESNT_EXISTS,
)


class TestProjectCreateSettingsAPI:
    def test_create_project(self, client, session):
        test_title = "test_project_1"
        test_data = {"title": test_title}
        resp = client.post(
            url_for("settings_project.project-create"),
            data=json.dumps(test_data),
        )
        project_id = (
            session.query(Project.id).filter_by(title=test_title).scalar()
        )
        assert resp.status_code == 200
        assert resp.json == {
            "success": True,
            "id": project_id,
            "title": test_title,
        }

    def test_create_project_with_exists_title(
        self, client, create_project_settings_test_data
    ):
        test_title = "test_project_1"
        test_data = {"title": test_title}
        resp = client.post(
            url_for("settings_project.project-create"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 400
        assert resp.json == {
            "error": EXC_PROJECT_ALREADY_EXISTS.format(test_title)
        }

    def test_create_project_with_wrong_parameters(self, client):
        test_title = "test_project_1"
        test_data = {"new_wrong_title": test_title}
        resp = client.post(
            url_for("settings_project.project-create"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 400
        assert resp.json == {"error": EXC_FIELD_IS_REQUIRED.format("title")}

    def test_create_project_with_not_valid_parameters(self, client):
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
            url_for("settings_project.project-create"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 400
        assert resp.json == {"error": test_error_text}


class TestProjectUpdateTitleSettingsAPI:
    def test_update_project(
        self, client, session, create_project_settings_test_data
    ):
        test_title = "test_new_title"
        test_project_id = 1
        test_data = {"id": test_project_id, "title": test_title}
        resp = client.put(
            url_for("settings_project.project-update-title"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 200
        assert resp.json == {"success": True}

    def test_update_project_when_it_doesnt_exists(self, client):
        test_title = "test_new_title"
        test_project_id = 101
        test_data = {"id": test_project_id, "title": test_title}
        resp = client.put(
            url_for("settings_project.project-update-title"),
            data=json.dumps(test_data),
        )

        assert resp.status_code == 400
        assert resp.json == {
            "error": EXC_PROJECT_DOESNT_EXISTS.format(test_project_id)
        }

    def test_update_project_with_wrong_parameters(self, client):
        test_title = "test_new_title"
        test_project_id = 1
        test_data = {"wrong_id": test_project_id, "title": test_title}
        resp = client.put(
            url_for("settings_project.project-update-title"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 400
        assert resp.json == {"error": EXC_FIELD_IS_REQUIRED.format("id")}

    def test_update_project_with_not_valid_parameters(self, client):
        test_error_text = [
            {
                "loc": ["id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
        test_title = "test_new_title"
        test_project_id = "wrong_id_type"
        test_data = {"id": test_project_id, "title": test_title}
        resp = client.put(
            url_for("settings_project.project-update-title"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 400
        assert resp.json == {"error": test_error_text}


class TestProjectDeleteSettingsAPI:
    def test_delete_project(self, client, create_project_settings_test_data):
        test_data = {"id": 1}
        resp = client.delete(
            url_for("settings_project.project-delete"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 200
        assert resp.json == {"success": True}

    def test_delete_project_when_it_doesnt_exists(self, client):
        test_data = {"id": 1}
        resp = client.delete(
            url_for("settings_project.project-delete"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 400
        assert resp.json == {
            "error": EXC_PROJECT_DOESNT_EXISTS.format(test_data.get("id"))
        }

    def test_delete_project_with_wrong_parameters(self, client):
        test_data = {"id_for_delete": 1}
        resp = client.delete(
            url_for("settings_project.project-delete"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 400
        assert resp.json == {"error": EXC_FIELD_IS_REQUIRED.format("id")}

    def test_delete_project_with_not_valid_parameters(self, client):
        test_error_text = [
            {
                "loc": ["id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
        test_data = {"id": "wrong_id"}
        resp = client.delete(
            url_for("settings_project.project-delete"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 400
        assert resp.json == {"error": test_error_text}


class TestProjectAttachToServicesGroupSettingsAPI:
    def test_attach_project(
        self,
        client,
        create_project_settings_test_data,
        create_services_group_test_data,
    ):
        test_project_id = 1
        test_services_group_id = 1
        test_data = {
            "project_id": test_project_id,
            "services_group_id": test_services_group_id,
        }
        resp = client.put(
            url_for("settings_project.project-attach"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 200
        assert resp.json == {"success": True}

    def test_attach_project_when_it_doesnt_exists(
        self, client, create_services_group_test_data
    ):
        test_project_id = 101
        test_services_group_id = 1
        test_data = {
            "project_id": test_project_id,
            "services_group_id": test_services_group_id,
        }
        resp = client.put(
            url_for("settings_project.project-attach"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 400
        assert resp.json == {
            "error": EXC_PROJECT_DOESNT_EXISTS.format(test_project_id)
        }

    def test_attach_project_when_services_group_doesnt_exists(
        self, client, create_project_settings_test_data
    ):
        test_project_id = 1
        test_services_group_id = 201
        test_data = {
            "project_id": test_project_id,
            "services_group_id": test_services_group_id,
        }
        resp = client.put(
            url_for("settings_project.project-attach"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 400
        assert resp.json == {
            "error": EXC_SERVICES_GROUP_DOESNT_EXISTS.format(
                test_services_group_id
            )
        }

    def test_attach_project_with_wrong_parameters(self, client):
        test_project_id = 1
        test_services_group_id = 1
        test_data = {
            "wrong_parameter": test_project_id,
            "services_group_id": test_services_group_id,
        }
        resp = client.put(
            url_for("settings_project.project-attach"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 400
        assert resp.json == {
            "error": EXC_FIELD_IS_REQUIRED.format("project_id")
        }

    def test_attach_project_with_not_valid_parameters(self, client):
        test_error_text = [
            {
                "loc": ["project_id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
        test_project_id = "not_valid_parameter"
        test_services_group_id = 1
        test_data = {
            "project_id": test_project_id,
            "services_group_id": test_services_group_id,
        }
        resp = client.put(
            url_for("settings_project.project-attach"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 400
        assert resp.json == {"error": test_error_text}


class TestProjectDetachFromServicesGroupSettingsAPI:
    def test_detach_project(
        self, client, create_project_services_group_test_data
    ):
        test_services_group_id = 2
        test_data = {"services_group_id": test_services_group_id}
        resp = client.put(
            url_for("settings_project.project-detach"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 200
        assert resp.json == {"success": True}

    def test_detach_project_when_services_group_doesnt_exists(
        self, client, create_project_settings_test_data
    ):
        test_services_group_id = 2
        test_data = {"services_group_id": test_services_group_id}
        resp = client.put(
            url_for("settings_project.project-detach"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 400
        assert resp.json == {
            "error": EXC_SERVICES_GROUP_DOESNT_EXISTS.format(
                test_services_group_id
            )
        }

    def test_detach_project_with_wrong_parameters(self, client):
        test_services_group_id = 2
        test_data = {"wrong_services_group_id": test_services_group_id}
        resp = client.put(
            url_for("settings_project.project-detach"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 400
        assert resp.json == {
            "error": EXC_FIELD_IS_REQUIRED.format("services_group_id")
        }

    def test_detach_project_with_not_valid_parameters(self, client):
        test_error_text = [
            {
                "loc": ["services_group_id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
        test_services_group_id = "not_valid_parameter"
        test_data = {"services_group_id": test_services_group_id}
        resp = client.put(
            url_for("settings_project.project-detach"),
            data=json.dumps(test_data),
        )
        assert resp.status_code == 400
        assert resp.json == {"error": test_error_text}
