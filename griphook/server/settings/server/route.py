from flask import Blueprint

from griphook.server.settings.server import views


settings_server_blueprint = Blueprint("settings_server", __name__)


settings_server_blueprint.add_url_rule(
    "/all", view_func=views.GetServers.as_view("servers-get-all")
)
settings_server_blueprint.add_url_rule(
    "/update_cpu_price",
    view_func=views.ServerUpdateCPUPrice.as_view("server-update-cpu-price"),
)
settings_server_blueprint.add_url_rule(
    "/update_memory_price",
    view_func=views.ServerUpdateMemoryPrice.as_view(
        "server-update-memory-price"
    ),
)
