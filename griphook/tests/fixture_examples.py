import pytest

from griphook.server import create_app, db as _db
from griphook.server.models import Cluster


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

    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope="function")
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
