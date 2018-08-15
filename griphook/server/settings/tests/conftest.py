import pytest

from griphook.server import db
from griphook.server import create_app
from griphook.server.models import Project, Team, Server, Cluster


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


@pytest.fixture
def create_team_settings_test_data(db_session):
    db_session.add_all(
        [
            Team(id=1, title='test_team_1'),
            Team(id=2, title='test_team_2'),
            Team(id=3, title='test_team_3')
        ]
    )
    db_session.commit()


@pytest.fixture
def create_server_settings_test_data(db_session):
    db_session.add_all(
        [
            Server(id=1, title='test_server_1'),
            Server(id=2, title='test_server_2'),
            Server(id=3, title='test_server_3', cpu_price=2.2, memory_price=1.8)
        ]
    )
    db_session.commit()


@pytest.fixture
def create_cluster_settings_test_data(db_session):
    db_session.add_all(
        [
            Cluster(id=1, title='test_cluster_1'),
            Cluster(id=2, title='test_cluster_2'),
            Cluster(id=3, title='test_cluster_3', cpu_price=1.4, memory_price=2.7)
        ]
    )
    db_session.commit()
