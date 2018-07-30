from flask import Blueprint

from . import views

average_load_blueprint = Blueprint('average_load', __name__, )

average_load_blueprint.add_url_rule('/server', view_func=views.ServerAverageLoadView.as_view('server'))
average_load_blueprint.add_url_rule('/services_group',
                                    view_func=views.ServicesGroupAverageLoadView.as_view('services_group'))
average_load_blueprint.add_url_rule('/service', view_func=views.ServiceAverageLoadView.as_view('service'))
