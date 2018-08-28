from flask import jsonify
from flask.views import View

from griphook.server import db
from griphook.server.settings.db import DataBase


class GetServicesGroupsProjectsTeams(View):
    methods = ["GET"]

    def dispatch_request(self):
        services_groups_query = DataBase.get_services_group(db.session)
        services_groups = [
            {
                "id": sg_id,
                "title": sg_title,
                "project_id": sg_project_id,
                "team_id": sg_team_id,
            }
            for (
                sg_id,
                sg_title,
                sg_project_id,
                sg_team_id,
            ) in services_groups_query
        ]

        projects_query = DataBase.get_projects(db.session)
        projects = [
            {"id": project_id, "title": project_title}
            for (project_id, project_title) in projects_query
        ]

        teams_query = DataBase.get_teams(db.session)
        teams = [
            {"id": team_id, "title": team_title}
            for (team_id, team_title) in teams_query
        ]

        return jsonify(
            {
                "services_groups": services_groups,
                "projects": projects,
                "teams": teams,
            }
        )
