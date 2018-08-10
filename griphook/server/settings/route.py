from flask import Blueprint

from griphook.server.settings import views


settings_blueprint = Blueprint('settings', __name__, )

settings_blueprint.add_url_rule('/', 'settings', view_func=views.index)
settings_blueprint.add_url_rule('/general', 'general', view_func=views.index)

settings_blueprint.add_url_rule('/project', view_func=views.ProjectSettingsAPI.as_view('project'))
