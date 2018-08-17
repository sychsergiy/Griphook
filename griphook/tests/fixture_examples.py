import pytest

from griphook.server import create_app, db as _db
from griphook.server.models import Cluster


# @pytest.fixture
# def app():
#     app = create_app()
#     app.config.from_object("griphook.server.config.TestingConfig")
#     return app
#
#
# @pytest.fixture
# def session(app):
#     session = _db.session
#     _db.drop_all()
#     _db.create_all()
#     session.commit()
#     yield session


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
