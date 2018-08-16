from flask import Blueprint

from griphook.server.billing import views


billing_blueprint = Blueprint("billing", __name__)


billing_blueprint.add_url_rule(
    "/get/service-group/metrics",
    "peaks-api",
    view_func=views.get_billing_metric_values_by_services_group,
    methods=("POST",),
)
billing_blueprint.add_url_rule(
    "/get/services_group/chart",
    "services-group-chart-api",
    view_func=views.get_metric_chart_for_services_group,
    methods=("POST",),
)
