from flask import Blueprint

from griphook.server.billing import views


billing_blueprint = Blueprint("billing", __name__)


billing_blueprint.add_url_rule(
    "/service-group-metrics",
    "peaks-api",
    view_func=views.get_billing_metric_values_by_services_group,
    methods=("POST",),
)
