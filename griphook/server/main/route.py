from flask import Blueprint

from . import views

main_blueprint = Blueprint('main', __name__, )

main_blueprint.add_url_rule('/', 'home', views.home)
