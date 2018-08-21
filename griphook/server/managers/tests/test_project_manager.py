import pytest

from sqlalchemy.sql import exists

from griphook.server.managers.exceptions import ProjectManagerException
from griphook.server.managers.project_manager import ProjectManager
from griphook.server.managers.constants import (
    EXC_SERVICES_GROUP_DOESNT_EXISTS,
    EXC_PROJECT_ALREADY_EXISTS,
    EXC_PROJECT_DOESNT_EXISTS,
)
from griphook.server.models import (
    ServicesGroup,
    MetricBilling,
    MetricPeak,
    Project,
)


class TestCreateProject:
    def test_create_project(self, db_session):
        test_title = "test_project_1"
        ProjectManager(db_session).create(title=test_title)
        assert db_session.query(
            exists().where(Project.title == test_title)
        ).scalar()

    def test_create_project_with_exists_title(
        self, db_session, create_project_team_test_data
    ):
        test_title = "test_project_1"
        with pytest.raises(ProjectManagerException) as excinfo:
            ProjectManager(db_session).create(title=test_title)
        assert EXC_PROJECT_ALREADY_EXISTS.format(test_title) in str(
            excinfo.value
        )


class TestUpdateProject:
    def test_update_project(self, db_session, create_project_team_test_data):
        test_new_title = "test_new_title"
        test_project_id = 1

        ProjectManager(db_session).update(
            project_id=test_project_id, new_title=test_new_title
        )
        project_title = (
            db_session.query(Project.title)
            .filter_by(id=test_project_id)
            .scalar()
        )
        assert project_title == test_new_title

    def test_update_project_when_it_doesnt_exists(self, db_session):
        test_new_title = "test_new_title"
        test_project_id = 1
        with pytest.raises(ProjectManagerException) as excinfo:
            ProjectManager(db_session).update(
                project_id=test_project_id, new_title=test_new_title
            )
        assert EXC_PROJECT_DOESNT_EXISTS.format(test_project_id) in str(
            excinfo.value
        )


class TestDeleteProject:
    def test_delete_project(self, db_session, create_project_team_test_data):
        test_project_id = 1
        ProjectManager(db_session).delete(project_id=test_project_id)
        assert not db_session.query(
            exists().where(Project.id == test_project_id)
        ).scalar()

    def test_delete_project_when_it_doesnt_exists(self, db_session):
        test_project_id = 1
        with pytest.raises(ProjectManagerException) as excinfo:
            ProjectManager(db_session).delete(project_id=test_project_id)
        assert EXC_PROJECT_DOESNT_EXISTS.format(test_project_id) in str(
            excinfo.value
        )


class TestAttachProject:
    def test_attach_project(self, db_session, create_project_team_test_data):
        test_project_id = 1
        test_services_group_id = 2
        ProjectManager(db_session).attach_to_services_group(
            project_id=test_project_id, services_group_id=test_services_group_id
        )
        services_group_project_id = (
            db_session.query(ServicesGroup.project_id)
            .filter_by(id=test_services_group_id)
            .scalar()
        )
        metrics_peaks_query = (
            db_session.query(MetricPeak)
            .filter_by(services_group_id=test_services_group_id)
            .all()
        )
        metrics_billing_query = (
            db_session.query(MetricBilling)
            .filter_by(services_group_id=test_services_group_id)
            .all()
        )
        assert services_group_project_id == test_project_id

        for metric_peaks in metrics_peaks_query:
            assert metric_peaks.project_id == test_project_id

        for metric_billing in metrics_billing_query:
            assert metric_billing.project_id == test_project_id

    def test_attach_project_when_it_doesnt_exists(self, db_session):
        test_project_id = 1
        test_services_group_id = 2
        with pytest.raises(ProjectManagerException) as excinfo:
            ProjectManager(db_session).attach_to_services_group(
                project_id=test_project_id,
                services_group_id=test_services_group_id,
            )
        assert EXC_PROJECT_DOESNT_EXISTS.format(test_project_id) in str(
            excinfo.value
        )

    def test_attach_project_when_services_group_doesnt_exists(
        self, db_session, create_project_team_test_data
    ):
        test_project_id = 1
        test_services_group_id = 201
        with pytest.raises(ProjectManagerException) as excinfo:
            ProjectManager(db_session).attach_to_services_group(
                project_id=test_project_id,
                services_group_id=test_services_group_id,
            )
        assert EXC_SERVICES_GROUP_DOESNT_EXISTS.format(
            test_services_group_id
        ) in str(excinfo.value)

    def test_attach_project_without_match_to_metric(
        self, db_session, create_project_team_test_data
    ):
        test_project_id = 1
        test_services_group_id = 3
        ProjectManager(db_session).attach_to_services_group(
            project_id=test_project_id, services_group_id=test_services_group_id
        )
        services_group_project_id = (
            db_session.query(ServicesGroup.project_id)
            .filter_by(id=test_services_group_id)
            .scalar()
        )
        metrics_peaks_query = (
            db_session.query(MetricPeak)
            .filter_by(services_group_id=test_services_group_id)
            .all()
        )
        metrics_billing_query = (
            db_session.query(MetricBilling)
            .filter_by(services_group_id=test_services_group_id)
            .all()
        )
        assert services_group_project_id == test_project_id
        assert not metrics_peaks_query
        assert not metrics_billing_query


class TestDetachProject:
    def test_detach_project(self, db_session, create_project_team_test_data):
        test_services_group_id = 4
        ProjectManager(db_session).detach_from_services_group(
            services_group_id=test_services_group_id
        )
        services_group_project_id = (
            db_session.query(ServicesGroup.project_id)
            .filter_by(id=test_services_group_id)
            .scalar()
        )
        metrics_peaks_query = (
            db_session.query(MetricPeak)
            .filter_by(services_group_id=test_services_group_id)
            .all()
        )
        metrics_billing_query = (
            db_session.query(MetricBilling)
            .filter_by(services_group_id=test_services_group_id)
            .all()
        )
        assert services_group_project_id is None

        for metric_peaks in metrics_peaks_query:
            assert metric_peaks.project_id is None

        for metric_billing in metrics_billing_query:
            assert metric_billing.project_id is None

    def test_detach_project_when_service_group_doesnt_exists(self, db_session):
        test_services_group_id = 4
        with pytest.raises(ProjectManagerException) as excinfo:
            ProjectManager(db_session).detach_from_services_group(
                services_group_id=test_services_group_id
            )
        assert EXC_SERVICES_GROUP_DOESNT_EXISTS.format(
            test_services_group_id
        ) in str(excinfo.value)
