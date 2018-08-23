from flask import Blueprint
from .views import LoginView

auth_blueprint = Blueprint("auth", __name__)

auth_blueprint.add_url_rule(
    "/login", "login", view_func=LoginView.as_view("login")
)
