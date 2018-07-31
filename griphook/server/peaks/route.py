from flask import Blueprint

from griphook.server.peaks import views

peaks_blueprint = Blueprint('peaks', __name__, )


peaks_blueprint.add_url_rule('/peaks', 'peaks', view_func=views.get_peacks, methods=("GET", "POST"))