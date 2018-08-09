import pytest

from sqlalchemy.sql import exists

from griphook.server.models import Metric, Project, ServicesGroup
from griphook.server.managers.exceptions import ProjectManagerException
from griphook.server.managers.project_manager import ProjectManager
from griphook.server.managers.constants import (
    EXC_SERVICES_GROUP_DOESNT_EXISTS,
    EXC_PROJECT_ALREADY_EXISTS,
    EXC_PROJECT_DOESNT_EXISTS
)


class TestCreateProject:
    def test_create_project(self, db_session):
        test_title = 'test_project_1'
        ProjectManager(db_session).create(title=test_title)
        assert db_session.query(exists().where(Project.title == test_title)).scalar()

    def test_create_project_with_exists_title(self, db_session, loading_test_data):
        test_title = 'test_project_1'
        with pytest.raises(ProjectManagerException) as excinfo:
            ProjectManager(db_session).create(title=test_title)
        assert EXC_PROJECT_ALREADY_EXISTS.format(test_title) in str(excinfo.value)


class TestUpdateProject:
    def test_update_project(self, db_session, loading_test_data):
        test_new_title = 'test_new_title'
        test_project_id = 1

        ProjectManager(db_session).update(project_id=test_project_id, new_title=test_new_title)
        project_title = db_session.query(Project.title).filter_by(id=test_project_id).scalar()
        assert project_title == test_new_title

    def test_update_project_when_it_doesnt_exists(self, db_session):
        test_new_title = 'test_new_title'
        test_project_id = 1
        with pytest.raises(ProjectManagerException) as excinfo:
            ProjectManager(db_session).update(project_id=test_project_id, new_title=test_new_title)
        assert EXC_PROJECT_DOESNT_EXISTS.format(test_project_id) in str(excinfo.value)


class TestDeleteProject:
    def test_delete_project(self, db_session, loading_test_data):
        test_project_id = 1
        ProjectManager(db_session).delete(project_id=test_project_id)
        assert not db_session.query(exists().where(Project.id == test_project_id)).scalar()

    def test_delete_project_when_it_doesnt_exists(self, db_session):
        test_project_id = 1
        with pytest.raises(ProjectManagerException) as excinfo:
            ProjectManager(db_session).delete(project_id=test_project_id)
        assert EXC_PROJECT_DOESNT_EXISTS.format(test_project_id) in str(excinfo.value)


class TestAttachProject:
    def test_attach_project(self, db_session, loading_test_data):
        test_project_id = 1
        test_services_group_id = 2
        ProjectManager(db_session).attach_to_services_group(project_id=test_project_id, services_group_id=test_services_group_id)

        services_group_project_id = db_session.query(ServicesGroup.project_id).filter_by(id=test_services_group_id).scalar()
        metrics = db_session.query(Metric).filter_by(services_group_id=test_services_group_id).all()

        assert services_group_project_id == test_project_id
        for metric in metrics:
            assert metric.project_id == test_project_id

    def test_attach_project_when_it_doesnt_exists(self, db_session):
        test_project_id = 1
        test_services_group_id = 2
        with pytest.raises(ProjectManagerException) as excinfo:
            ProjectManager(db_session).attach_to_services_group(project_id=test_project_id,services_group_id=test_services_group_id)
        assert EXC_PROJECT_DOESNT_EXISTS.format(test_project_id) in str(excinfo.value)


    def test_attach_project_when_services_group_doesnt_exists(self, db_session, loading_test_data):
        test_project_id = 1
        test_services_group_id = 201
        with pytest.raises(ProjectManagerException) as excinfo:
            ProjectManager(db_session).attach_to_services_group(project_id=test_project_id,services_group_id=test_services_group_id)
        assert EXC_SERVICES_GROUP_DOESNT_EXISTS.format(test_services_group_id) in str(excinfo.value)


    def test_attach_project_without_match_to_metric(self, db_session, loading_test_data):
        test_project_id = 1
        test_services_group_id = 3
        ProjectManager(db_session).attach_to_services_group(project_id=test_project_id,services_group_id=test_services_group_id)

        services_group_project_id = db_session.query(ServicesGroup.project_id).filter_by(id=test_services_group_id).scalar()
        metrics = db_session.query(Metric).filter_by(services_group_id=test_services_group_id).all()

        assert services_group_project_id == test_project_id
        assert not metrics


class TestDetachProject:
    def test_detach_project(self, db_session, loading_test_data):
        test_services_group_id = 4
        ProjectManager(db_session).detach_from_services_group(services_group_id=test_services_group_id)

        services_group_project_id = db_session.query(ServicesGroup.project_id).filter_by(id=test_services_group_id).scalar()
        metrics = db_session.query(Metric).filter_by(services_group_id=test_services_group_id).all()

        assert services_group_project_id is None
        for metric in metrics:
            assert metric.project_id is None

    def test_detach_project_when_services_group_doesnt_exists(self, db_session):
        test_services_group_id = 4
        with pytest.raises(ProjectManagerException) as excinfo:
            ProjectManager(db_session).detach_from_services_group(services_group_id=test_services_group_id)
        assert EXC_SERVICES_GROUP_DOESNT_EXISTS.format(test_services_group_id) in str(excinfo.value)
