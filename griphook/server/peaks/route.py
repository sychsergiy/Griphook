from flask import Blueprint

from . import views

peaks_blueprint = Blueprint('peaks', __name__, )

peaks_blueprint.add_url_rule('/', 'peaks', views.index)