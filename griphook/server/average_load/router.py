from flask import Blueprint

from . import views

average_load_blueprint = Blueprint('average_load', __name__, )

server_average_load_view = views.ServerAverageLoadView.as_view('server')
services_group_average_load_view = views.ServicesGroupAverageLoadView.as_view('services_group')
services_average_load_view = views.ServiceAverageLoadView.as_view('service')

average_load_blueprint.add_url_rule('/server', view_func=server_average_load_view)
average_load_blueprint.add_url_rule('/services_group', view_func=services_group_average_load_view)
average_load_blueprint.add_url_rule('/service', view_func=services_average_load_view)
