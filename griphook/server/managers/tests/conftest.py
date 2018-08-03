import pytest

from griphook.server import db
from griphook.server import create_app
from griphook.server.models import Project, ServicesGroup, Metric


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object('griphook.server.config.TestingConfig')
    return app


@pytest.fixture
def db_session(app):
    session = db.session
    db.drop_all()
    db.create_all()
    session.commit()
    yield session


@pytest.fixture
def loading_test_data(db_session):
    db_session.add_all(
        [
            Project(id=1, title='test_project_1'),
            Project(id=2, title='test_project_2'),
            Project(id=3, title='test_project_3'),

            ServicesGroup(id=1, title='test_services_group_1'),
            ServicesGroup(id=2, title='test_services_group_2'),
            ServicesGroup(id=3, title='test_services_group_3'),
            ServicesGroup(id=4, title='test_services_group_4', project_id=2),

            Metric(id=1, services_group_id=1),
            Metric(id=2, services_group_id=2),
            Metric(id=3, services_group_id=2),
            Metric(id=4, services_group_id=2),
            Metric(id=5, services_group_id=4, project_id=2),
            Metric(id=6, services_group_id=4, project_id=2),
            Metric(id=7, services_group_id=4, project_id=2)
        ]
    )
    db_session.commit()
