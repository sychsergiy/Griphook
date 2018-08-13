import pytest

from griphook.server import create_app
from griphook.server import db as _db
from griphook.server.models import Cluster, Server


@pytest.fixture(scope="session")
def app(request):
    app = create_app()
    app.config.from_object("griphook.server.config.TestingConfig")

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session")
def db(app, request):
    """Session-wide test database."""

    # def teardown():
    #     _db.drop_all()

    _db.app = app
    # _db.create_all()

    # request.addfinalizer(teardown)
    # TODO: uncomment finalizer
    return _db


@pytest.fixture(scope="session")
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope="function")
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


@pytest.fixture(scope="function")
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

    return Server.query.with_entities(Server.id, Server.title, Server.cluster_id).all()
