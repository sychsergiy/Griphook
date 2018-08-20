from flask import Blueprint

from . import views

filters_blueprint = Blueprint("filters", __name__)

filters_blueprint.add_url_rule(
    "/peaks_hierarchy", "peaks", views.get_peaks_filters_hierarchy
)

filters_blueprint.add_url_rule(
    "/billing_hierarchy", "billing", views.get_billing_filters_hierarchy
)
