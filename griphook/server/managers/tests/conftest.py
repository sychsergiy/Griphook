import pytest

from griphook.server import db
from griphook.server import create_app
from griphook.server.models import ServicesGroup, Project, Cluster, Server, Team
from griphook.tests.base_fixtures import app, client, client_class, session


@pytest.fixture
def create_project_team_test_data(session):
    session.add_all(
        [
            Project(id=1, title="test_project_1"),
            Project(id=2, title="test_project_2"),
            Project(id=3, title="test_project_3"),
        ]
    )
    session.commit()
    session.add_all(
        [
            Team(id=1, title="test_team_1"),
            Team(id=2, title="test_team_2"),
            Team(id=3, title="test_team_3"),
        ]
    )
    session.commit()
    session.add_all(
        [
            ServicesGroup(id=1, title="test_services_group_1"),
            ServicesGroup(id=2, title="test_services_group_2"),
            ServicesGroup(id=3, title="test_services_group_3"),
            ServicesGroup(id=4, title="test_services_group_4", project_id=2),
        ]
    )
    session.commit()


@pytest.fixture
def create_server_cluster_test_data(session):
    session.add_all(
        [
            Server(id=1, title="test_server_1", cpu_price=2.4, memory_price=6),
            Server(id=2, title="test_server_2"),
        ]
    )
    session.add_all(
        [
            Cluster(id=1, title="test_cluster_1", cpu_price=3, memory_price=2),
            Cluster(id=2, title="test_cluster_2"),
        ]
    )
    session.commit()
