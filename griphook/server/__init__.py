

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, verify_jwt_in_request

# instantiate the extensions
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__, static_folder="../frontend/dist")
    # set config
    app_settings = os.getenv(
        "APP_SETTINGS", "griphook.server.config.DevelopmentConfig"
    )
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    # register blueprints
    from griphook.server.billing import billing_blueprint

    app.register_blueprint(billing_blueprint, url_prefix="/billing")

    ##########################################################################
    # PROTECTED FROM UNAUTHORIZED USERS                                      #
    ##########################################################################
    from griphook.server.settings import settings_blueprint

    settings_blueprint.before_request(verify_jwt_in_request)
    app.register_blueprint(settings_blueprint, url_prefix="/settings")

    from griphook.server.settings.project import settings_project_blueprint

    settings_project_blueprint.before_request(verify_jwt_in_request)
    app.register_blueprint(
        settings_project_blueprint, url_prefix="/settings/project"
    )

    from griphook.server.settings.team import settings_team_blueprint

    settings_team_blueprint.before_request(verify_jwt_in_request)
    app.register_blueprint(settings_team_blueprint, url_prefix="/settings/team")

    from griphook.server.settings.server import settings_server_blueprint

    settings_server_blueprint.before_request(verify_jwt_in_request)
    app.register_blueprint(
        settings_server_blueprint, url_prefix="/settings/server"
    )

    from griphook.server.settings.cluster import settings_cluster_blueprint

    settings_cluster_blueprint.before_request(verify_jwt_in_request)
    app.register_blueprint(
        settings_cluster_blueprint, url_prefix="/settings/cluster"
    )

    ##########################################################################
    # END PROTECTION                                                         #
    ##########################################################################

    from griphook.server.filters import filters_blueprint

    app.register_blueprint(filters_blueprint, url_prefix="/filters")

    from griphook.server.peaks import peaks_blueprint

    app.register_blueprint(peaks_blueprint, url_prefix="/peaks")

    from griphook.server.average_load import average_load_blueprint

    app.register_blueprint(average_load_blueprint, url_prefix="/average_load")

    from griphook.server.auth import auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
