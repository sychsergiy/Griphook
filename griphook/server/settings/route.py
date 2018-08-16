from flask import Blueprint

from griphook.server.settings import views


settings_blueprint = Blueprint('settings', __name__, )

# routes for project settings API
settings_blueprint.add_url_rule('/project/v1/get-all', view_func=views.GetProjects.as_view('project_get_all'))
settings_blueprint.add_url_rule('/project/v1/create', view_func=views.ProjectCreate.as_view('project_create'))
settings_blueprint.add_url_rule('/project/v1/update-title', view_func=views.ProjectUpdateTitle.as_view('project_update_title'))
settings_blueprint.add_url_rule('/project/v1/delete', view_func=views.ProjectDelete.as_view('project_delete'))
settings_blueprint.add_url_rule('/project/v1/attach', view_func=views.ProjectAttachToServicesGroup.as_view('project_attach'))
settings_blueprint.add_url_rule('/project/v1/detach', view_func=views.ProjectDetachFromServicesGroup.as_view('project_detach'))

# routes for team settings API
settings_blueprint.add_url_rule('/team/v1/get-all', view_func=views.GetTeams.as_view('teams_get_all'))
settings_blueprint.add_url_rule('/team/v1/create', view_func=views.TeamCreate.as_view('team_create'))
settings_blueprint.add_url_rule('/team/v1/update-title', view_func=views.TeamUpdateTitle.as_view('team_update_title'))
settings_blueprint.add_url_rule('/team/v1/delete', view_func=views.TeamDelete.as_view('team_delete'))
settings_blueprint.add_url_rule('/team/v1/attach', view_func=views.TeamAttachToServicesGroup.as_view('team_attach'))
settings_blueprint.add_url_rule('/team/v1/detach', view_func=views.TeamDetachFromServicesGroup.as_view('team_detach'))

# routes for server settings API
settings_blueprint.add_url_rule('/server/v1/get-all', view_func=views.GetServers.as_view('servers_get_all'))
settings_blueprint.add_url_rule('/server/v1/update-cpu-price', view_func=views.ServerUpdateCPUPrice.as_view('server_update_cpu_price'))
settings_blueprint.add_url_rule('/server/v1/update-memory-price', view_func=views.ServerUpdateMemoryPrice.as_view('server_update_memory_price'))

# routes for cluster settings API
settings_blueprint.add_url_rule('/cluster/v1/get-all', view_func=views.GetClusters.as_view('clusters_get_all'))
settings_blueprint.add_url_rule('/cluster/v1/update-cpu-price', view_func=views.ClusterUpdateCPUPrice.as_view('cluster_update_cpu_price'))
settings_blueprint.add_url_rule('/cluster/v1/update-memory-price', view_func=views.ClusterUpdateMemoryPrice.as_view('cluster_update_memory_price'))
