from datetime import datetime, timedelta
import pytest

from griphook.server.models import (MetricBilling, Team, Project, Cluster,
                                    BatchStoryBilling, Service, ServicesGroup, Server)

from griphook.tests.base_fixtures import session, app

TIME_FORMAT = "%Y-%m-%d"


@pytest.fixture(scope="function")
def clusters(session):
    clusters = [Cluster(title="test1")]
    session.add_all(clusters)
    session.commit()
    return Cluster.query.with_entities(Cluster.id, Cluster.title)


@pytest.fixture(scope="function")
def teams(session):
    teams = [Team(title="test1"), Team(title="test2")]
    session.add_all(teams)
    session.commit()
    return Team.query.with_entities(Team.id, Team.title)


@pytest.fixture(scope="function")
def projects(session):
    project1 = Project(title="test1")
    project2 = Project(title="test2")
    session.add_all([project1, project2])
    session.commit()
    return Project.query.with_entities(Project.id, Project.title)


@pytest.fixture(scope="function")
def servers(session, clusters):
    cluster1, *_ = clusters
    server1 = Server(title="test1", cluster_id=cluster1.id)
    server2 = Server(title="test2", cluster_id=cluster1.id)
    session.add_all([server1, server2])
    session.commit()
    return Server.query.with_entities(Server.id, Server.title)


@pytest.fixture(scope="function")
def services_groups(session, teams, projects):
    team1, team2, *_ = teams
    project1, project2, *_ = projects
    services_group1 = ServicesGroup(title="test1", project_id=project1.id, team_id=team1.id)
    services_group2 = ServicesGroup(title="test2", project_id=project2.id, team_id=team2.id)
    session.add_all([services_group1, services_group2])
    session.commit()
    return ServicesGroup.query.with_entities(
        ServicesGroup.id, ServicesGroup.title
    )


@pytest.fixture(scope="function")
def services(session, servers, services_groups):
    services_group1, services_group2, *_ = services_groups
    server1, server2, *_ = servers
    service1 = Service(
        title="service1",
        instance="test",
        server_id=server1.id,
        services_group_id=services_group1.id,
    )
    service2 = Service(
        title="service2",
        instance="test",
        server_id=server1.id,
        services_group_id=services_group2.id,
    )
    service3 = Service(
        title="service3",
        instance="test",
        server_id=server2.id,
        services_group_id=services_group2.id,
    )
    session.add_all([service1, service2, service3])
    session.commit()
    return Service.query.with_entities(Service.id, Service.title)


@pytest.fixture(scope="function")
def billing_batch_stories(session):
    time1 = datetime.now() - timedelta(days=8)
    time2 = datetime.now()
    batches_story1 = BatchStoryBilling(time=time1)
    batches_story2 = BatchStoryBilling(time=time2)
    session.add_all([batches_story1, batches_story2])
    session.commit()
    return BatchStoryBilling.query.with_entities(
        BatchStoryBilling.id, BatchStoryBilling.time
    )


@pytest.fixture(scope="function")
def metrics(session, services, services_groups, billing_batch_stories):
    billing_batch_story1, billing_batch_story2, *_ = billing_batch_stories
    service1, service2, service3, *_ = services
    services_group1, services_group2, *_ = services_groups

    metric1 = MetricBilling(
        value=1,
        batch_id=billing_batch_story1.id,
        service_id=service1.id,
        services_group_id=services_group1.id,
        type="user_cpu_percent",
    )
    metric2 = MetricBilling(
        value=2,
        batch_id=billing_batch_story2.id,
        service_id=service2.id,
        services_group_id=services_group2.id,
        type="user_cpu_percent",
    )
    metric3 = MetricBilling(
        value=30,
        batch_id=billing_batch_story2.id,
        service_id=service3.id,
        services_group_id=services_group2.id,
        type="vsize",
    )
    metric4 = MetricBilling(
        value=4,
        batch_id=billing_batch_story1.id,
        service_id=service3.id,
        services_group_id=services_group2.id,
        type="vsize",
    )
    session.add_all([metric1, metric2, metric3, metric4])
    session.commit()
    return MetricBilling.query.with_entities(MetricBilling.id, MetricBilling.type, MetricBilling.value)


@pytest.fixture(scope="function")
def billing_table_endpoint_request_data(billing_batch_stories, servers):
    data = {
        "target_type": "all",
        "target_ids": [],
        "time_from": billing_batch_stories[0].time.strftime(TIME_FORMAT),
        "time_until": billing_batch_stories[1].time.strftime(TIME_FORMAT),
    }
    return data
