from flask import Blueprint

from . import views

filters_blueprint = Blueprint('filters', __name__, )

filters_blueprint.add_url_rule('/servers', 'servers', views.servers_api_view)
filters_blueprint.add_url_rule('/service_groups', 'service_groups', views.services_groups_api_view)
filters_blueprint.add_url_rule('/services', 'services', views.services_api_view)

filters_blueprint.add_url_rule('/clusters', 'clusters', views.clusters_api_view)
