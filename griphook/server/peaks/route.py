from flask import Blueprint

from griphook.server.peaks import views

peaks_blueprint = Blueprint("peaks", __name__)

peaks_blueprint.add_url_rule("/", "peaks", views.index)
peaks_blueprint.add_url_rule(
    "/get/chart",
    "peaks-api",
    view_func=views.get_peaks_for_chart,
    methods=("POST",),
)
