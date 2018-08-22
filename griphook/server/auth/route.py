from flask import Blueprint
from griphook.server.auth.views import login

auth_blueprint = Blueprint("auth", __name__)

auth_blueprint.add_url_rule("/login", "login", login)
