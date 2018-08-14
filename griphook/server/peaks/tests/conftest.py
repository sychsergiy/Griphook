from datetime import datetime, timedelta
import pytest

from griphook.server import create_app, db as _db
from griphook.server.models import (
    Cluster,
    Server,
    Service,
    ServicesGroup,
    MetricPeak,
    BatchStoryPeaks,
)
from griphook.server.peaks.constants import REQUEST_DATE_TIME_FORMAT


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
    clusters = [Cluster(title="test1")]
    session.add_all(clusters)
    session.commit()
    return Cluster.query.with_entities(Cluster.id, Cluster.title)


@pytest.fixture(scope="function")
def servers(session, clusters):
    cluster1, *_ = clusters
    server1 = Server(title="test1", cluster_id=cluster1.id)
    server2 = Server(title="test2", cluster_id=cluster1.id)
    session.add_all([server1, server2])
    session.commit()
    return Server.query.with_entities(Server.id, Server.title)


@pytest.fixture(scope="function")
def services_groups(session, clusters):
    cluster1, *_ = clusters
    services_group1 = ServicesGroup(title="test1")
    services_group2 = ServicesGroup(title="test2")
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
def batch_stories(session):
    time1 = datetime.now() - timedelta(days=8)
    time2 = datetime.now()
    batches_story1 = BatchStoryPeaks(time=time1)
    batches_story2 = BatchStoryPeaks(time=time2)
    session.add_all([batches_story1, batches_story2])
    session.commit()
    return BatchStoryPeaks.query.with_entities(
        BatchStoryPeaks.id, BatchStoryPeaks.time
    )


@pytest.fixture(scope="function")
def metrics(session, services, services_groups, batch_stories):
    batches_story1, batches_story2, *_ = batch_stories
    service1, service2, service3, *_ = services
    services_group1, services_group2, *_ = services_groups

    metric1 = MetricPeak(
        value=2,
        batch_id=batches_story1.id,
        service_id=service1.id,
        services_group_id=services_group1.id,
        type="user_cpu_percent",
    )
    metric2 = MetricPeak(
        value=2,
        batch_id=batches_story2.id,
        service_id=service2.id,
        services_group_id=services_group2.id,
        type="user_cpu_percent",
    )
    metric3 = MetricPeak(
        value=3,
        batch_id=batches_story2.id,
        service_id=service3.id,
        services_group_id=services_group2.id,
        type="user_cpu_percent",
    )
    metric4 = MetricPeak(
        value=4,
        batch_id=batches_story1.id,
        service_id=service3.id,
        services_group_id=services_group2.id,
        type="user_cpu_percent",
    )
    session.add_all([metric1, metric2, metric3, metric4])
    session.commit()
    return MetricPeak.query.with_entities(MetricPeak.id, MetricPeak.value)


@pytest.fixture(scope="function")
def peaks_endpoint_request_data(batch_stories, servers):
    data = {
        "target_type": "server",
        "target_id": servers[1].id,
        "metric_type": "user_cpu_percent",
        "step": 1,
        "time_from": batch_stories[0].time.strftime(REQUEST_DATE_TIME_FORMAT),
        "time_until": batch_stories[1].time.strftime(REQUEST_DATE_TIME_FORMAT),
    }
    return data
