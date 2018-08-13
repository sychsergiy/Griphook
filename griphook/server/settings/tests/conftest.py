import pytest

from griphook.server import db
from griphook.server import create_app
from griphook.server.models import Project


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object('griphook.server.config.TestingConfig')
    return app


@pytest.fixture
def db_session(app):
    session = db.session
    db.drop_all()
    db.create_all()
    session.commit()
    yield session


@pytest.fixture
def create_project_settings_test_data(db_session):
    db_session.add_all(
        [
            Project(id=1, title='test_project_1'),
            Project(id=2, title='test_project_2'),
            Project(id=3, title='test_project_3')
        ]
    )
    db_session.commit()
