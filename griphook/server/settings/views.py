import json

from flask import request, jsonify
from flask.views import View
from pydantic import ValidationError

from griphook.server import db
from griphook.server.settings.db import DataBase
from griphook.server.managers.project_manager import ProjectManager
from griphook.server.managers.team_manager import TeamManager
from griphook.server.managers.server_manager import ServerManager
from griphook.server.managers.cluster_manager import ClusterManager

from griphook.server.settings.validators import (
    AttachDetachProjectTeamModel,
    UpdateServerClusterModel,
    UpdateProjectTeamModel
)
from griphook.server.managers.exceptions import (
    ProjectManagerException,
    TeamManagerException,
    ServerManagerException,
    ClusterManagerException
)
from griphook.server.settings.constants import (
    EXC_FIELD_IS_REQUIRED,
    PARAMETERS_PROJECT_TEAM,
    PARAMETERS_ATTACH_TEAM,
    PARAMETERS_ATTACH_PROJECT,
    PARAMETERS_DETACH_PROJECT_TEAM,
    PARAMETERS_SERVER_CLUSTER_CPU_PRICE,
    PARAMETERS_SERVER_CLUSTER_MEMORY_PRICE
)


class GetServicesGroupsProjectsTeams(View):
    methods = ['GET']

    def dispatch_request(self):
        services_groups_query = DataBase.get_services_group(db.session)
        services_groups = [{"id": services_groups_id, "title": services_groups_title} for (services_groups_id, services_groups_title) in services_groups_query]

        projects_query = DataBase.get_projects(db.session)
        projects = [{"id": project_id, "title": project_title} for (project_id, project_title) in projects_query]

        teams_query = DataBase.get_teams(db.session)
        teams = [{"id": team_id, "title": team_title} for (team_id, team_title) in teams_query]

        return jsonify(
            {
                'services_groups': services_groups,
                'projects': projects,
                'teams': teams
            }
        )


class GetProjects(View):
    methods = ['GET']

    def dispatch_request(self):
        projects_query = DataBase.get_projects(db.session)
        projects = [{"id": project_id, "title": project_title} for (project_id, project_title) in projects_query]
        return jsonify(
            {'projects': projects}
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
            )
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
        )


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
            )
        return jsonify(
            {'error': EXC_FIELD_IS_REQUIRED.format('id')}
        ), 400


class ProjectAttachToServicesGroup(View):
    methods = ['PUT']

    def dispatch_request(self):
        data_for_attach = json.loads(request.data)

        for parameter in PARAMETERS_ATTACH_PROJECT:
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
            ProjectManager(db.session).attach_to_services_group(project_id=valid_data_for_attach.project_id, services_group_id=valid_data_for_attach.services_group_id)
        except ProjectManagerException as exc:
            return jsonify(
                {'error': exc.error_text}
            ), 400
        return jsonify(
            {'success': True}
        )


class ProjectDetachFromServicesGroup(View):
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
            ProjectManager(db.session).detach_from_services_group(services_group_id=valid_data_for_detach.services_group_id)
        except ProjectManagerException as exc:
            return jsonify(
                {'error': exc.error_text}
            ), 400
        return jsonify(
            {'success': True}
        )


class GetTeams(View):
    methods = ['GET']

    def dispatch_request(self):
        teams_query = DataBase.get_teams(db.session)
        teams = [{"id": team_id, "title": team_title} for (team_id, team_title) in teams_query]
        return jsonify(
            {'teams': teams}
        )


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
            )
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
        )


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
            )
        return jsonify(
            {'error': EXC_FIELD_IS_REQUIRED.format('id')}
        ), 400


class TeamAttachToServicesGroup(View):
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


class GetServers(View):
    methods = ['GET']

    def dispatch_request(self):
        servers_query = DataBase.get_servers(db.session)
        servers = [{"id": server_id, "title": server_title} for (server_id, server_title) in servers_query]
        return jsonify(
            {'servers': servers}
        )


class ServerUpdateCPUPrice(View):
    methods = ['PUT']

    def dispatch_request(self):
        data_for_update = json.loads(request.data)

        for parameter in PARAMETERS_SERVER_CLUSTER_CPU_PRICE:
            if parameter not in data_for_update:
                return jsonify(
                    {'error': EXC_FIELD_IS_REQUIRED.format(parameter)}
                ), 400
        try:
            valid_data_for_create = UpdateServerClusterModel(**data_for_update)
        except ValidationError as e:
            return jsonify(
                {'error': e.errors()}
            ), 400
        try:
            ServerManager(db.session).set_cpu_price(
                server_id=valid_data_for_create.id,
                new_cpu_price=valid_data_for_create.cpu_price
            )
        except ServerManagerException as exc:
            return jsonify(
                {'error': exc.error_text}
            ), 400
        return jsonify(
            {'success': True}
        )


class ServerUpdateMemoryPrice(View):
    methods = ['PUT']

    def dispatch_request(self):
        data_for_update = json.loads(request.data)

        for parameter in PARAMETERS_SERVER_CLUSTER_MEMORY_PRICE:
            if parameter not in data_for_update:
                return jsonify(
                    {'error': EXC_FIELD_IS_REQUIRED.format(parameter)}
                ), 400
        try:
            valid_data_for_create = UpdateServerClusterModel(**data_for_update)
        except ValidationError as e:
            return jsonify(
                {'error': e.errors()}
            ), 400
        try:
            ServerManager(db.session).set_memory_price(
                server_id=valid_data_for_create.id,
                new_memory_price=valid_data_for_create.memory_price
            )
        except ServerManagerException as exc:
            return jsonify(
                {'error': exc.error_text}
            ), 400
        return jsonify(
            {'success': True}
        )


class GetClusters(View):
    methods = ['GET']

    def dispatch_request(self):
        clusters_query = DataBase.get_clusters(db.session)
        clusters = [{"id": cluster_id, "title": cluster_title} for (cluster_id, cluster_title) in clusters_query]
        return jsonify(
            {'clusters': clusters}
        )


class ClusterUpdateCPUPrice(View):
    methods = ['PUT']

    def dispatch_request(self):
        data_for_update = json.loads(request.data)

        for parameter in PARAMETERS_SERVER_CLUSTER_CPU_PRICE:
            if parameter not in data_for_update:
                return jsonify(
                    {'error': EXC_FIELD_IS_REQUIRED.format(parameter)}
                ), 400
        try:
            valid_data_for_create = UpdateServerClusterModel(**data_for_update)
        except ValidationError as e:
            return jsonify(
                {'error': e.errors()}
            ), 400
        try:
            ClusterManager(db.session).set_cpu_price(
                cluster_id=valid_data_for_create.id,
                new_cpu_price=valid_data_for_create.cpu_price
            )
        except ClusterManagerException as exc:
            return jsonify(
                {'error': exc.error_text}
            ), 400
        return jsonify(
            {'success': True}
        )


class ClusterUpdateMemoryPrice(View):
    methods = ['PUT']

    def dispatch_request(self):
        data_for_update = json.loads(request.data)

        for parameter in PARAMETERS_SERVER_CLUSTER_MEMORY_PRICE:
            if parameter not in data_for_update:
                return jsonify(
                    {'error': EXC_FIELD_IS_REQUIRED.format(parameter)}
                ), 400
        try:
            valid_data_for_create = UpdateServerClusterModel(**data_for_update)
        except ValidationError as e:
            return jsonify(
                {'error': e.errors()}
            ), 400
        try:
            ClusterManager(db.session).set_memory_price(
                cluster_id=valid_data_for_create.id,
                new_memory_price=valid_data_for_create.memory_price
            )
        except ClusterManagerException as exc:
            return jsonify(
                {'error': exc.error_text}
            ), 400
        return jsonify(
            {'success': True}
        )
