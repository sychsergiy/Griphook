from flask import Blueprint

from griphook.server.settings.team import views


settings_team_blueprint = Blueprint('settings_team', __name__, )


settings_team_blueprint.add_url_rule('/get-all', view_func=views.GetTeams.as_view('teams_get_all'))
settings_team_blueprint.add_url_rule('/create', view_func=views.TeamCreate.as_view('team_create'))
settings_team_blueprint.add_url_rule('/update-title', view_func=views.TeamUpdateTitle.as_view('team_update_title'))
settings_team_blueprint.add_url_rule('/delete', view_func=views.TeamDelete.as_view('team_delete'))
settings_team_blueprint.add_url_rule('/attach', view_func=views.TeamAttachToServicesGroup.as_view('team_attach'))
settings_team_blueprint.add_url_rule('/detach', view_func=views.TeamDetachFromServicesGroup.as_view('team_detach'))
