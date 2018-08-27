from flask import Blueprint

from griphook.server.settings.project import views


settings_project_blueprint = Blueprint('settings_project', __name__, )


settings_project_blueprint.add_url_rule('/all', view_func=views.GetProjects.as_view('project-get-all'))
settings_project_blueprint.add_url_rule('/create', view_func=views.ProjectCreate.as_view('project-create'))
settings_project_blueprint.add_url_rule('/update_title', view_func=views.ProjectUpdateTitle.as_view('project-update-title'))
settings_project_blueprint.add_url_rule('/delete', view_func=views.ProjectDelete.as_view('project-delete'))
settings_project_blueprint.add_url_rule('/attach', view_func=views.ProjectAttachToServicesGroup.as_view('project-attach'))
settings_project_blueprint.add_url_rule('/detach', view_func=views.ProjectDetachFromServicesGroup.as_view('project-detach'))
