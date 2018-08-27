from flask import Blueprint

from griphook.server.settings.server import views


settings_server_blueprint = Blueprint('settings_server', __name__, )


settings_server_blueprint.add_url_rule('/get-all', view_func=views.GetServers.as_view('servers_get_all'))
settings_server_blueprint.add_url_rule('/update-cpu-price', view_func=views.ServerUpdateCPUPrice.as_view('server_update_cpu_price'))
settings_server_blueprint.add_url_rule('/update-memory-price', view_func=views.ServerUpdateMemoryPrice.as_view('server_update_memory_price'))
