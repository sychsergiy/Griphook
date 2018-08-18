from flask import Blueprint

from . import pie_chart_views

billing_blueprint = Blueprint("billing", __name__)

billing_blueprint.add_url_rule(
    "/get_pie_chart_absolute_data",
    view_func=pie_chart_views.GetPieChartAbsoluteDataView.as_view("get-pie-chart-absolute-data")
)

billing_blueprint.add_url_rule(
    "/get_pie_chart_relative_data",
    view_func=pie_chart_views.GetPieChartRelativeDataView.as_view("get-pie-chart-relative-data")
)
