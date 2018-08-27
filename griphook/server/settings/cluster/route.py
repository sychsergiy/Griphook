from flask import Blueprint

from griphook.server.settings.cluster import views


settings_cluster_blueprint = Blueprint('settings_cluster', __name__, )


settings_cluster_blueprint.add_url_rule('/get-all', view_func=views.GetClusters.as_view('clusters_get_all'))
settings_cluster_blueprint.add_url_rule('/update-cpu-price', view_func=views.ClusterUpdateCPUPrice.as_view('cluster_update_cpu_price'))
settings_cluster_blueprint.add_url_rule('/update-memory-price', view_func=views.ClusterUpdateMemoryPrice.as_view('cluster_update_memory_price'))
