import pytest

from griphook.server.models import (
    Cluster,
    Server,
    Project,
    Team,
    Service,
    ServicesGroup,
)

from griphook.tests.base_fixtures import app, client, client_class, session


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
    (cluster1_id, *_), (cluster2_id, *_), (cluster3_id, *_), *_ = clusters

    servers = [
        Server(title="Server1", cluster_id=cluster1_id),
        Server(title="Server2", cluster_id=cluster1_id),
        Server(title="Server3", cluster_id=cluster2_id),
        Server(title="Server4", cluster_id=cluster3_id),
    ]

    session.add_all(servers)
    session.commit()

    return Server.query.with_entities(
        Server.id, Server.title, Server.cluster_id
    ).all()


@pytest.fixture
def projects(session):
    """save Projects instances to db"""
    projects = [
        Project(title="project1"),
        Project(title="project2"),
        Project(title="project3"),
    ]
    session.add_all(projects)
    session.commit()
    return Project.query.with_entities(Project.id, Project.title)


@pytest.fixture
def teams(session):
    """save Teams instances to db"""

    teams = [Team(title="team1"), Team(title="team2"), Team(title="team3")]
    session.add_all(teams)
    session.commit()
    return Team.query.with_entities(Team.id, Team.title)


@pytest.fixture
def services_groups_with_servers_and_clusters(session, servers, clusters):
    """
    save ServicesGroups instances with
    server_id and cluster_id foreign keys
    ServicesGroups attached to servers through services
    """
    (server1_id, *_), (server2_id, *_), (server3_id, *_), *_ = servers
    session.add_all(
        [ServicesGroup(title="group1"), ServicesGroup(title="group2")]
    )
    session.commit()

    session.add_all(
        [
            Service(
                title="service1",
                server_id=server1_id,
                services_group_id=1,
                instance=0,
            ),
            Service(
                title="service2",
                server_id=server1_id,
                services_group_id=1,
                instance=0,
            ),
            Service(
                title="service3",
                server_id=server2_id,
                services_group_id=1,
                instance=0,
            ),
            Service(
                title="service4",
                server_id=server3_id,
                services_group_id=1,
                instance=0,
            ),
            Service(
                title="service5",
                server_id=server3_id,
                services_group_id=2,
                instance=0,
            ),
        ]
    )
    session.commit()
