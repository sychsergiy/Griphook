from flask import Blueprint

from . import views

filters_blueprint = Blueprint("filters", __name__)

filters_blueprint.add_url_rule(
    "/hierarchy", "hierarchy", views.filters_hierarchy_api_view
)
