from datetime import datetime, timedelta
import pytest
import random

from griphook.server import create_app, db as _db
from griphook.server.models import (
    MetricBilling,
    Team,
    Project,
    Cluster,
    BatchStoryBilling,
    Service,
    ServicesGroup,
    Server,
)


from griphook.server.billing.constants import REQUEST_DATE_TIME_FORMAT


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


@pytest.fixture(scope="function")
def clusters(session):
    clusters = [Cluster(title="cluster_" + str(i)) for i in range(1, 21)]
    session.add_all(clusters)
    session.commit()
    return Cluster.query.with_entities(Cluster.id, Cluster.title)


@pytest.fixture(scope="function")
def teams(session):
    teams = [Team(title="team_" + str(i)) for i in range(1, 21)]
    session.add_all(teams)
    session.commit()
    return Team.query.with_entities(Team.id, Team.title)


@pytest.fixture(scope="function")
def projects(session):
    projects = [Project(title="project_" + str(i)) for i in range(1, 21)]
    session.add_all(projects)
    session.commit()
    return Project.query.with_entities(Project.id, Project.title)


@pytest.fixture(scope="function")
def servers(session, clusters):
    servers = []
    for i, cluster in enumerate(clusters, start=1):
        servers.append(Server(title="server_" + str(i), cluster_id=cluster.id))
    session.add_all(servers)
    session.commit()
    return Server.query.with_entities(Server.id, Server.title)


@pytest.fixture(scope="function")
def services_groups(session, teams, projects):
    services_groups = []
    for i, t in enumerate(zip(projects, teams), start=1):
        services_groups.append(
            ServicesGroup(
                title="services_group_" + str(i), project_id=t[0].id, team_id=t[1].id
            )
        )
    session.add_all(services_groups)
    session.commit()
    return ServicesGroup.query.with_entities(
        ServicesGroup.id, ServicesGroup.title
    )


@pytest.fixture(scope="function")
def services(session, servers, services_groups):
    services = []
    for i, t in enumerate(zip(servers, services_groups), start=1):
        print()
        services.append(
            Service(
                title="service_" + str(i),
                instance="test_instance",
                server_id=t[0].id,
                services_group_id=t[1].id
            )
        )
    session.add_all(services)
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
    billing_batch_story1, billing_batch_story2 = billing_batch_stories
    batch_stories = [billing_batch_story1, billing_batch_story2] * 40

    metrics = []
    for i in zip(services, services_groups):
        metrics.append(MetricBilling(
            value=random.randint(1, 30),
            batch_id=batch_stories.pop().id,
            service_id=i[0].id,
            services_group_id=i[1].id,
            type="user_cpu_percent"
        ))

    for i in zip(services, services_groups):
        metrics.append(MetricBilling(
            value=random.randint(1, 30),
            batch_id=batch_stories.pop().id,
            service_id=i[0].id,
            services_group_id=i[1].id,
            type="vsize"
        ))
    session.add_all(metrics)
    session.commit()
    return MetricBilling.query.with_entities(
        MetricBilling.id, MetricBilling.type, MetricBilling.value
    )


@pytest.fixture(scope="function")
def billing_table_endpoint_request_data(billing_batch_stories, servers):
    data = {
        "target_type": "cluster",
        "target_ids": [1, 2, 3, 4, 5, 6],
        "time_from": billing_batch_stories[0].time.strftime(
            REQUEST_DATE_TIME_FORMAT
        ),
        "time_until": billing_batch_stories[1].time.strftime(
            REQUEST_DATE_TIME_FORMAT
        ),
        "page": 1,
    }
    return data
