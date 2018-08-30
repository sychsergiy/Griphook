import pytest

from griphook.server import db
from griphook.server import create_app
from griphook.server.models import Project, Team, Server, Cluster, ServicesGroup
from griphook.tests.base_fixtures import app, client, session


@pytest.fixture
def create_project_settings_test_data(session):
    session.add_all(
        [
            Project(id=1, title="test_project_1"),
            Project(id=2, title="test_project_2"),
            Project(id=3, title="test_project_3"),
        ]
    )
    session.commit()


@pytest.fixture
def create_team_settings_test_data(session):
    session.add_all(
        [
            Team(id=1, title="test_team_1"),
            Team(id=2, title="test_team_2"),
            Team(id=3, title="test_team_3"),
        ]
    )
    session.commit()


@pytest.fixture
def create_server_settings_test_data(session):
    session.add_all(
        [
            Server(id=1, title="test_server_1"),
            Server(id=2, title="test_server_2"),
            Server(
                id=3, title="test_server_3", cpu_price=2.2, memory_price=1.8
            ),
        ]
    )
    session.commit()


@pytest.fixture
def create_cluster_settings_test_data(session):
    session.add_all(
        [
            Cluster(id=1, title="test_cluster_1"),
            Cluster(id=2, title="test_cluster_2"),
            Cluster(
                id=3, title="test_cluster_3", cpu_price=1.4, memory_price=2.7
            ),
        ]
    )
    session.commit()


@pytest.fixture
def create_services_group_test_data(session):
    session.add_all(
        [
            ServicesGroup(id=1, title="test_services_group_1"),
            ServicesGroup(id=2, title="test_services_group_2"),
            ServicesGroup(id=3, title="test_services_group_3"),
        ]
    )
    session.commit()


@pytest.fixture
def create_project_services_group_test_data(session):
    session.add_all(
        [
            Project(id=1, title="test_project_1"),
            Project(id=2, title="test_project_2"),
        ]
    )
    session.commit()
    session.add_all(
        [
            ServicesGroup(id=1, title="test_services_group_1", project_id=1),
            ServicesGroup(id=2, title="test_services_group_2", project_id=2),
        ]
    )
    session.commit()
