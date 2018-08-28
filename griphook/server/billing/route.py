from flask import Blueprint

from . import views
from . import pie_chart_views

billing_blueprint = Blueprint("billing", __name__)

billing_blueprint.add_url_rule(
    "/get_filtered_table_data",
    "get-filtered-billing-table-data",
    view_func=views.get_filtered_billing_table_data,
    methods=("POST",),
)

billing_blueprint.add_url_rule(
    "/get_service_group_metrics/user_cpu_percent/",
    "services-group-user-cpu-percent",
    view_func=views.get_servcies_group_cpu_metrics,
    methods=("POST",),
)

billing_blueprint.add_url_rule(
    "/get_service_group_metrics/vsize/",
    "services-group-vsize",
    view_func=views.get_services_group_vsize_metrics,
    methods=("POST",),
)

billing_blueprint.add_url_rule(
    "/get_pie_chart_absolute_data",
    view_func=pie_chart_views.GetPieChartAbsoluteDataView.as_view(
        "get-pie-chart-absolute-data"
    ),
)

billing_blueprint.add_url_rule(
    "/get_pie_chart_relative_data",
    view_func=pie_chart_views.GetPieChartRelativeDataView.as_view(
        "get-pie-chart-relative-data"
    ),
)
