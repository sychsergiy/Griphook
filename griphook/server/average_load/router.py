from flask import Blueprint

from . import views

average_load_blueprint = Blueprint("average_load", __name__)

average_load_chart_data_view = views.AverageLoadChartDataView.as_view("chart_data")

average_load_blueprint.add_url_rule(
    "/chart_data", view_func=average_load_chart_data_view
)
