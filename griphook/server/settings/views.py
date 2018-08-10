import json

from flask.views import MethodView
from flask import request, abort, render_template, jsonify, Response

from griphook.server import db
from griphook.server.models import Project
from griphook.server.managers.project_manager import ProjectManager
from griphook.server.managers.exceptions import ProjectManagerException


class ProjectSettingsAPI(MethodView):
    def post(self):
        data = json.loads(request.data)
        try:
            new_project = ProjectManager(db.session).create(data.get('title'))
        except ProjectManagerException as exc:
            abort(400, exc)

        return jsonify(
            {
                'id': new_project.id,
                'title': new_project.title
            }
        )

    def put(self):
        pass

    def delete(self):
        data = json.loads(request.data)
        try:
            ProjectManager(db.session).delete(data.get('id'))
        except ProjectManagerException as exc:
            abort(400, exc)

        return Response(status=200)


def index():
    session = db.session
    projects = session.query(Project).all()
    return render_template('settings/general.html', projects=projects)
