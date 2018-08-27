from flask import Blueprint

from griphook.server.settings import views


settings_blueprint = Blueprint('settings', __name__, )


settings_blueprint.add_url_rule('/all-servicesgroups-projects-teams', view_func=views.GetServicesGroupsProjectsTeams.as_view('all-servicesgroups-projects-teams'))
