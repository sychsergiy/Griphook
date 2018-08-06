# griphook/server/__init__.py


import os

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# instantiate the extensions
toolbar = DebugToolbarExtension()
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()


def create_app(script_info=None):
    # instantiate the app
    app = Flask(
        __name__,
        template_folder='../client/templates',
        static_folder='../client/static'
    )

    # set config
    app_settings = os.getenv(
        'APP_SETTINGS', 'griphook.server.config.DevelopmentConfig')
    app.config.from_object(app_settings)

    # set up extensions
    toolbar.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # register blueprints
    from griphook.server.main import main_blueprint
    app.register_blueprint(main_blueprint)

    from griphook.server.billing import billing_blueprint
    app.register_blueprint(billing_blueprint, url_prefix='/billing')

    from griphook.server.admin import admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from griphook.server.filters import filters_blueprint
    app.register_blueprint(filters_blueprint, url_prefix='/filters')

    from griphook.server.peaks import peaks_blueprint
    app.register_blueprint(peaks_blueprint, url_prefix='/peaks')

    # set up error handlers
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/500.html'), 500

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
