from flask_testing import TestCase

from griphook.server import db, create_app

app = create_app()


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object("griphook.server.config.TestingConfig")
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
