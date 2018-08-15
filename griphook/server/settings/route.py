from flask import Blueprint

from griphook.server.settings import views


settings_blueprint = Blueprint('settings', __name__, )

# routes for project settings API
settings_blueprint.add_url_rule('/project/v1/create', view_func=views.ProjectCreate.as_view('project_create'))
settings_blueprint.add_url_rule('/project/v1/update-title', view_func=views.ProjectUpdateTitle.as_view('project_update_title'))
settings_blueprint.add_url_rule('/project/v1/delete', view_func=views.ProjectDelete.as_view('project_delete'))
# routes for team settings API
settings_blueprint.add_url_rule('/team/v1/create', view_func=views.TeamCreate.as_view('team_create'))
settings_blueprint.add_url_rule('/team/v1/update-title', view_func=views.TeamUpdateTitle.as_view('team_update_title'))
settings_blueprint.add_url_rule('/team/v1/delete', view_func=views.TeamDelete.as_view('team_delete'))
