import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, verify_jwt_in_request

# instantiate the extensions
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)


def set_up_extensions(app):
    jwt.init_app(app)
    bcrypt.init_app(app)


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__, static_folder="../frontend/dist")
    # set config
    app_settings = os.getenv(
        "APP_SETTINGS", "griphook.server.config.DevelopmentConfig"
    )
    app.config.from_object(app_settings)

    # set up extensions and db
    init_db(app)
    set_up_extensions(app)

    # import blueprints
    from griphook.server.billing import billing_blueprint
    from griphook.server.settings import settings_blueprint
    from griphook.server.settings.project import settings_project_blueprint
    from griphook.server.settings.team import settings_team_blueprint
    from griphook.server.settings.server import settings_server_blueprint
    from griphook.server.settings.cluster import settings_cluster_blueprint
    from griphook.server.auth import auth_blueprint
    from griphook.server.average_load import average_load_blueprint
    from griphook.server.peaks import peaks_blueprint
    from griphook.server.filters import filters_blueprint

    # Prevent tests to fail with wrong status code assertion
    if not app.config.get("TESTING"):
        # PROTECT SETTINGS FROM UNAUTHORIZED USERS
        settings_blueprint.before_request(verify_jwt_in_request)
        settings_project_blueprint.before_request(verify_jwt_in_request)
        settings_team_blueprint.before_request(verify_jwt_in_request)
        settings_server_blueprint.before_request(verify_jwt_in_request)
        settings_cluster_blueprint.before_request(verify_jwt_in_request)

    # Billing
    app.register_blueprint(billing_blueprint, url_prefix="/billing")

    # Settings
    app.register_blueprint(settings_blueprint, url_prefix="/settings")
    app.register_blueprint(
        settings_project_blueprint, url_prefix="/settings/project"
    )
    app.register_blueprint(settings_team_blueprint, url_prefix="/settings/team")
    app.register_blueprint(
        settings_server_blueprint, url_prefix="/settings/server"
    )
    app.register_blueprint(
        settings_cluster_blueprint, url_prefix="/settings/cluster"
    )

    # Filters
    app.register_blueprint(filters_blueprint, url_prefix="/filters")

    # Peaks
    app.register_blueprint(peaks_blueprint, url_prefix="/peaks")

    # Average load
    app.register_blueprint(average_load_blueprint, url_prefix="/average_load")

    # Auth
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
