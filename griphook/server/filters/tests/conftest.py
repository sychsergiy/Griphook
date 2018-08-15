import pytest

from griphook.server import create_app, db as _db
from griphook.server.models import Cluster, Server, Project, Team


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object("griphook.server.config.TestingConfig")
    return app


@pytest.fixture
def session(app):
    session = _db.session
    _db.drop_all()
    _db.create_all()
    session.commit()
    yield session


@pytest.fixture
def clusters(session):
    """save Cluster instances to db"""
    clusters = [
        Cluster(title="cluster1"),
        Cluster(title="cluster2"),
        Cluster(title="cluster3"),
        Cluster(title="cluster4"),
    ]
    session.add_all(clusters)
    session.commit()
    return Cluster.query.with_entities(Cluster.id, Cluster.title)


@pytest.fixture
def servers(session, clusters: tuple):
    """save Servers instances to db"""
    (cluster1_id, _), (cluster2_id, _), *_ = clusters

    servers = [
        Server(title="Server1", cluster_id=cluster1_id),
        Server(title="Server2", cluster_id=cluster1_id),
        Server(title="Server3", cluster_id=cluster2_id),
    ]

    session.add_all(servers)
    session.commit()

    return Server.query.with_entities(
        Server.id, Server.title, Server.cluster_id
    ).all()


@pytest.fixture
def projects(session):
    """save Projects instances to db"""
    clusters = [
        Project(title="project1"),
        Project(title="project2"),
        Project(title="project3"),
    ]
    session.add_all(clusters)
    session.commit()
    return Project.query.with_entities(Project.id, Project.title)


@pytest.fixture
def teams(session):
    """save Teams instances to db"""
    teams = [
        Team(title="project1"),
        Team(title="project2"),
        Team(title="project3"),
    ]
    session.add_all(teams)
    session.commit()
    return Team.query.with_entities(Team.id, Team.title)
