from flask import Blueprint

from griphook.server.billing import views


billing_blueprint = Blueprint("billing", __name__)


billing_blueprint.add_url_rule(
    "/get_service_group_metrics",
    "metrics-api",
    view_func=views.get_billing_metric_values_by_services_group,
    methods=("POST",),
)
billing_blueprint.add_url_rule(
    "/get_services_group_chart",
    "services-group-chart_api",
    view_func=views.get_metric_chart_for_services_group,
    methods=("POST",),
)
