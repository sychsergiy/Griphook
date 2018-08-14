from flask import Blueprint

from griphook.server.settings import views


settings_blueprint = Blueprint('settings', __name__, )

# routes for settings page
settings_blueprint.add_url_rule('/', 'settings', view_func=views.index)
settings_blueprint.add_url_rule('/general', 'general', view_func=views.index)

# routes for settings API
settings_blueprint.add_url_rule('/project', view_func=views.ProjectSettingsAPI.as_view('project'))
settings_blueprint.add_url_rule('/team', view_func=views.TeamSettingsAPI.as_view('team'))
# settings_blueprint.add_url_rule('/server', view_func=views.ServerSettingsAPI.as_view('server'))
# settings_blueprint.add_url_rule('/cluster', view_func=views.ClusterSettingsAPI.as_view('cluster'))
