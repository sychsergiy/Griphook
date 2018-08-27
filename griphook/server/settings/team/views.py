import json

from flask import request, jsonify
from flask.views import View
from pydantic import ValidationError

from griphook.server import db
from griphook.server.settings.db import DataBase
from griphook.server.managers.team_manager import TeamManager

from griphook.server.settings.validators import (
    AttachDetachProjectTeamModel,
    UpdateProjectTeamModel
)
from griphook.server.managers.exceptions import TeamManagerException
from griphook.server.settings.constants import (
    EXC_FIELD_IS_REQUIRED,
    PARAMETERS_PROJECT_TEAM,
    PARAMETERS_ATTACH_TEAM,
    PARAMETERS_DETACH_PROJECT_TEAM,
)


class GetTeams(View):
    """
    API method for getting all teams.
    """
    methods = ['GET']

    def dispatch_request(self):
        teams_query = DataBase.get_teams(db.session)
        teams = [{"id": team_id, "title": team_title} for (team_id, team_title) in teams_query]
        return jsonify(
            {'teams': teams}
        )


class TeamCreate(View):
    """
    API method for create new team instance.

    Incoming data format:
    {
        "title": string | required
    }

    If the incoming data is not valid or the name already exists,
    the error information will be returned.

    Result data format:
    {
        "success": boolean,
        "id": integer,
        "title": string
    }
    """
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
            )
        return jsonify(
            {'error': EXC_FIELD_IS_REQUIRED.format('title')}
        ), 400


class TeamUpdateTitle(View):
    """
    API method for update team title.

    Incoming data format:
    {
        "id": integer | required
        "title": string | required
    }

    If the incoming data is not valid or team doesn't exists,
    the error information will be returned.

    Result data format:
    {
        "success": boolean
    }
    """
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
        )


class TeamDelete(View):
    """
    API method for delete team instance.

    Incoming data format:
    {
        "id": integer | required
    }

    If the incoming data is not valid or team doesn't exists,
    the error information will be returned.

    Result data format:
    {
        "success": boolean
    }
    """
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
            )
        return jsonify(
            {'error': EXC_FIELD_IS_REQUIRED.format('id')}
        ), 400


class TeamAttachToServicesGroup(View):
    """
    API method for attach team to services_group.

    Incoming data format:
    {
        "project_id": integer | required,
        "services_group_id": integer | required
    }

    If the incoming data is not valid, team or services_group doesn't exists,
    the error information will be returned.

    Result data format:
    {
        "success": boolean
    }
    """
    methods = ['PUT']

    def dispatch_request(self):
        data_for_attach = json.loads(request.data)

        for parameter in PARAMETERS_ATTACH_TEAM:
            if parameter not in data_for_attach:
                return jsonify(
                    {'error': EXC_FIELD_IS_REQUIRED.format(parameter)}
                ), 400
        try:
            valid_data_for_attach = AttachDetachProjectTeamModel(**data_for_attach)
        except ValidationError as e:
            return jsonify(
                {'error': e.errors()}
            ), 400
        try:
            TeamManager(db.session).attach_to_services_group(team_id=valid_data_for_attach.team_id, services_group_id=valid_data_for_attach.services_group_id)
        except TeamManagerException as exc:
            return jsonify(
                {'error': exc.error_text}
            ), 400
        return jsonify(
            {'success': True}
        )


class TeamDetachFromServicesGroup(View):
    """
    API method for detach team from services_group.

    Incoming data format:
    {
        "services_group_id": integer | required
    }

    If the incoming data is not valid or services_group doesn't exists,
    the error information will be returned.

    Result data format:
    {
        "success": boolean
    }
    """
    methods = ['PUT']

    def dispatch_request(self):
        data_for_detach = json.loads(request.data)

        for parameter in PARAMETERS_DETACH_PROJECT_TEAM:
            if parameter not in data_for_detach:
                return jsonify(
                    {'error': EXC_FIELD_IS_REQUIRED.format(parameter)}
                ), 400
        try:
            valid_data_for_detach = AttachDetachProjectTeamModel(**data_for_detach)
        except ValidationError as e:
            return jsonify(
                {'error': e.errors()}
            ), 400
        try:
            TeamManager(db.session).detach_from_services_group(services_group_id=valid_data_for_detach.services_group_id)
        except TeamManagerException as exc:
            return jsonify(
                {'error': exc.error_text}
            ), 400
        return jsonify(
            {'success': True}
        )
