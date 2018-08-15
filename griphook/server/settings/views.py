import json

from flask import request, jsonify
from flask.views import View
from pydantic import ValidationError

from griphook.server import db
from griphook.server.managers.project_manager import ProjectManager
from griphook.server.managers.team_manager import TeamManager

from griphook.server.settings.validators import (
    UpdateProjectTeamModel
)
from griphook.server.managers.exceptions import (
    ProjectManagerException,
    TeamManagerException
)
from griphook.server.settings.constants import (
    EXC_FIELD_IS_REQUIRED,
    PARAMETERS_PROJECT_TEAM
)


class ProjectCreate(View):
    methods = ['POST']

    def dispatch_request(self):
        data_for_create = json.loads(request.data)

        if 'title' in data_for_create:
            try:
                valid_data_for_create = UpdateProjectTeamModel(**data_for_create)
            except ValidationError as e:
                return jsonify(
                    {'error': e.errors()}
                ), 400
            try:
                new_project = ProjectManager(db.session).create(
                    title=valid_data_for_create.title
                )
            except ProjectManagerException as exc:
                return jsonify(
                    {'error': exc.error_text}
                ), 400
            return jsonify(
                {
                    'success': True,
                    'id': new_project.id,
                    'title': new_project.title
                }
            ), 200
        return jsonify(
            {'error': EXC_FIELD_IS_REQUIRED.format('title')}
        ), 400


class ProjectUpdateTitle(View):
    methods = ['PUT']

    def dispatch_request(self):
        data_for_update = json.loads(request.data)

        for parameter in PARAMETERS_PROJECT_TEAM:
            if parameter not in data_for_update:
                return jsonify(
                    {'error': EXC_FIELD_IS_REQUIRED.format(parameter)}
                ), 400
        try:
            valid_data_for_update = UpdateProjectTeamModel(**data_for_update)
        except ValidationError as e:
            return jsonify(
                    {'error': e.errors()}
                ), 400
        try:
            ProjectManager(db.session).update(
                project_id=valid_data_for_update.id,
                new_title=valid_data_for_update.title
            )
        except ProjectManagerException as exc:
            return jsonify(
                {'error': exc.error_text}
            ), 400
        return jsonify(
            {'success': True}
        ), 200


class ProjectDelete(View):
    methods = ['DELETE']

    def dispatch_request(self):
        data_for_delete = json.loads(request.data)

        if 'id' in data_for_delete:
            try:
                valid_data_for_delete = UpdateProjectTeamModel(**data_for_delete)
            except ValidationError as e:
                return jsonify(
                    {'error': e.errors()}
                ), 400
            try:
                ProjectManager(db.session).delete(
                    project_id=valid_data_for_delete.id
                )
            except ProjectManagerException as exc:
                return jsonify(
                    {'error': exc.error_text}
                ), 400
            return jsonify(
                {'success': True}
            ), 200
        return jsonify(
            {'error': EXC_FIELD_IS_REQUIRED.format('id')}
        ), 400


class TeamCreate(View):
    methods = ['POST']

    def dispatch_request(self):
        data_for_create = json.loads(request.data)

        if 'title' in data_for_create:
            try:
                valid_data_for_create = UpdateProjectTeamModel(**data_for_create)
            except ValidationError as e:
                return jsonify(
                    {'error': e.errors()}
                ), 400
            try:
                new_team = TeamManager(db.session).create(
                    title=valid_data_for_create.title
                )
            except TeamManagerException as exc:
                return jsonify(
                    {'error': exc.error_text}
                ), 400
            return jsonify(
                {
                    'success': True,
                    'id': new_team.id,
                    'title': new_team.title
                }
            ), 200
        return jsonify(
            {'error': EXC_FIELD_IS_REQUIRED.format('title')}
        ), 400


class TeamUpdateTitle(View):
    methods = ['PUT']

    def dispatch_request(self):
        data_for_update = json.loads(request.data)

        for parameter in PARAMETERS_PROJECT_TEAM:
            if parameter not in data_for_update:
                return jsonify(
                    {'error': EXC_FIELD_IS_REQUIRED.format(parameter)}
                ), 400
        try:
            valid_data_for_update = UpdateProjectTeamModel(**data_for_update)
        except ValidationError as e:
            return jsonify(
                    {'error': e.errors()}
                ), 400
        try:
            TeamManager(db.session).update(
                team_id=valid_data_for_update.id,
                new_title=valid_data_for_update.title
            )
        except TeamManagerException as exc:
            return jsonify(
                {'error': exc.error_text}
            ), 400
        return jsonify(
            {'success': True}
        ), 200


class TeamDelete(View):
    methods = ['DELETE']

    def dispatch_request(self):
        data_for_delete = json.loads(request.data)

        if 'id' in data_for_delete:
            try:
                valid_data_for_delete = UpdateProjectTeamModel(**data_for_delete)
            except ValidationError as e:
                return jsonify(
                    {'error': e.errors()}
                ), 400
            try:
                TeamManager(db.session).delete(
                    team_id=valid_data_for_delete.id
                )
            except TeamManagerException as exc:
                return jsonify(
                    {'error': exc.error_text}
                ), 400
            return jsonify(
                {'success': True}
            ), 200
        return jsonify(
            {'error': EXC_FIELD_IS_REQUIRED.format('id')}
        ), 400
