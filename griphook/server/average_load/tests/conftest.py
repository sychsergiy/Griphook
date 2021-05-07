import pytest

from griphook.server.models import Cluster, Server

from griphook.tests.base_fixtures import app, session, client, client_class


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

    return Server.query.with_entities(
        Server.id, Server.title, Server.cluster_id
    ).all()
