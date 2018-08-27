from flask import Blueprint

from griphook.server.settings.cluster import views


settings_cluster_blueprint = Blueprint('settings_cluster', __name__, )


settings_cluster_blueprint.add_url_rule('/all', view_func=views.GetClusters.as_view('clusters-get-all'))
settings_cluster_blueprint.add_url_rule('/update_cpu_price', view_func=views.ClusterUpdateCPUPrice.as_view('cluster-update-cpu-price'))
settings_cluster_blueprint.add_url_rule('/update_memory_price', view_func=views.ClusterUpdateMemoryPrice.as_view('cluster-update-memory-price'))
