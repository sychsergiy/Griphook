from flask import Blueprint

from . import views
from . import pie_chart_views

billing_blueprint = Blueprint('billing', __name__, )

billing_blueprint.add_url_rule(
    '/get_filtered_table_data',
    'get_filtered_billing_table_data',
    view_func=views.get_filtered_billing_table_data,
    methods=("POST",)
)

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

billing_blueprint.add_url_rule(
    "/get_pie_chart_absolute_data",
    view_func=pie_chart_views.GetPieChartAbsoluteDataView.as_view("get-pie-chart-absolute-data")
)

billing_blueprint.add_url_rule(
    "/get_pie_chart_relative_data",
    view_func=pie_chart_views.GetPieChartRelativeDataView.as_view("get-pie-chart-relative-data")
)
