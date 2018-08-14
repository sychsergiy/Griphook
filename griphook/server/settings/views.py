import json

from flask.views import MethodView
from flask import request, render_template, jsonify

from griphook.server import db
from griphook.server.models import Project, Team
from griphook.server.managers.project_manager import ProjectManager
from griphook.server.managers.team_manager import TeamManager
from griphook.server.managers.server_manager import ServerManager

from griphook.server.managers.exceptions import (
    ProjectManagerException,
    TeamManagerException,
    ServerManagerException
)


class ProjectSettingsAPI(MethodView):
    def post(self):
        data = json.loads(request.data)
        try:
            new_project = ProjectManager(db.session).create(data.get('title'))
        except ProjectManagerException as exc:
            return jsonify({'error': exc.error_text}), 400
        return jsonify(
            {
                'success': True,
                'id': new_project.id,
                'title': new_project.title
            }
        ), 200

    def put(self):
        data = json.loads(request.data)
        try:
            ProjectManager(db.session).update(data.get('id'), data.get('title'))
        except ProjectManagerException as exc:
            return jsonify({'error': exc.error_text}), 400
        return jsonify({'success': True}), 200

    def delete(self):
        data = json.loads(request.data)
        try:
            ProjectManager(db.session).delete(data.get('id'))
        except ProjectManagerException as exc:
            return jsonify({'error': exc.error_text}), 400
        return jsonify({'success': True}), 200


class TeamSettingsAPI(MethodView):
    def post(self):
        data = json.loads(request.data)
        try:
            new_team = TeamManager(db.session).create(data.get('title'))
        except TeamManagerException as exc:
            return jsonify({'error': exc.error_text}), 400

        return jsonify(
            {
                'success': True,
                'id': new_team.id,
                'title': new_team.title
            }
        ), 200

    def put(self):
        data = json.loads(request.data)
        try:
            TeamManager(db.session).update(data.get('id'), data.get('title'))
        except TeamManagerException as exc:
            return jsonify({'error': exc.error_text}), 400
        return jsonify({'success': True}), 200

    def delete(self):
        data = json.loads(request.data)
        try:
            TeamManager(db.session).delete(data.get('id'))
        except TeamManagerException as exc:
            return jsonify({'error': exc.error_text}), 400
        return jsonify({'success': True}), 200



def index():
    session = db.session
    projects = session.query(Project).all()
    teams = session.query(Team).all()
    return render_template('settings/general.html', projects=projects, teams=teams)
