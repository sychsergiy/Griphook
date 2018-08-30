import pytest

from sqlalchemy.sql import exists

from griphook.server.managers.exceptions import TeamManagerException
from griphook.server.managers.team_manager import TeamManager
from griphook.server.managers.constants import (
    EXC_SERVICES_GROUP_DOESNT_EXISTS,
    EXC_TEAM_ALREADY_EXISTS,
    EXC_TEAM_DOESNT_EXISTS,
)
from griphook.server.models import (
    ServicesGroup,
    Team,
)


class TestCreateTeam:
    def test_create_team(self, db_session):
        test_title = "test_team_1"
        TeamManager(db_session).create(title=test_title)
        assert db_session.query(
            exists().where(Team.title == test_title)
        ).scalar()

    def test_create_team_with_exists_title(
        self, db_session, create_project_team_test_data
    ):
        test_title = "test_team_1"
        with pytest.raises(TeamManagerException) as exc:
            TeamManager(db_session).create(title=test_title)
        assert EXC_TEAM_ALREADY_EXISTS.format(test_title) in str(exc.value)


class TestUpdateTeam:
    def test_update_team(self, db_session, create_project_team_test_data):
        test_new_title = "test_new_title"
        test_team_id = 1

        TeamManager(db_session).update(
            team_id=test_team_id, new_title=test_new_title
        )
        team_title = (
            db_session.query(Team.title).filter_by(id=test_team_id).scalar()
        )
        assert team_title == test_new_title

    def test_update_team_when_it_doesnt_exists(self, db_session):
        test_new_title = "test_new_title"
        test_team_id = 1
        with pytest.raises(TeamManagerException) as exc:
            TeamManager(db_session).update(
                team_id=test_team_id, new_title=test_new_title
            )
        assert EXC_TEAM_DOESNT_EXISTS.format(test_team_id) in str(exc.value)


class TestDeleteTeam:
    def test_delete_team(self, db_session, create_project_team_test_data):
        test_team_id = 1
        TeamManager(db_session).delete(team_id=test_team_id)
        assert not db_session.query(
            exists().where(Team.id == test_team_id)
        ).scalar()

    def test_delete_team_when_it_doesnt_exists(self, db_session):
        test_team_id = 1
        with pytest.raises(TeamManagerException) as exc:
            TeamManager(db_session).delete(team_id=test_team_id)
        assert EXC_TEAM_DOESNT_EXISTS.format(test_team_id) in str(exc.value)


class TestAttachTeam:
    def test_attach_team(self, db_session, create_project_team_test_data):
        test_team_id = 1
        test_services_group_id = 2
        TeamManager(db_session).attach_to_services_group(
            team_id=test_team_id, services_group_id=test_services_group_id
        )
        services_group_team_id = (
            db_session.query(ServicesGroup.team_id)
            .filter_by(id=test_services_group_id)
            .scalar()
        )
        assert services_group_team_id == test_team_id

    def test_attach_team_when_it_doesnt_exists(self, db_session):
        test_team_id = 1
        test_services_group_id = 2
        with pytest.raises(TeamManagerException) as exc:
            TeamManager(db_session).attach_to_services_group(
                team_id=test_team_id, services_group_id=test_services_group_id
            )
        assert EXC_TEAM_DOESNT_EXISTS.format(test_team_id) in str(exc.value)

    def test_attach_team_when_services_group_doesnt_exists(
        self, db_session, create_project_team_test_data
    ):
        test_team_id = 1
        test_services_group_id = 201
        with pytest.raises(TeamManagerException) as exc:
            TeamManager(db_session).attach_to_services_group(
                team_id=test_team_id, services_group_id=test_services_group_id
            )
        assert EXC_SERVICES_GROUP_DOESNT_EXISTS.format(
            test_services_group_id
        ) in str(exc.value)

    def test_attach_team_without_match_to_metric(
        self, db_session, create_project_team_test_data
    ):
        test_team_id = 1
        test_services_group_id = 3
        TeamManager(db_session).attach_to_services_group(
            team_id=test_team_id, services_group_id=test_services_group_id
        )
        services_group_team_id = (
            db_session.query(ServicesGroup.team_id)
            .filter_by(id=test_services_group_id)
            .scalar()
        )
        assert services_group_team_id == test_team_id


class TestDetachTeam:
    def test_detach_team(self, db_session, create_project_team_test_data):
        test_services_group_id = 4
        TeamManager(db_session).detach_from_services_group(
            services_group_id=test_services_group_id
        )
        services_group_team_id = (
            db_session.query(ServicesGroup.team_id)
            .filter_by(id=test_services_group_id)
            .scalar()
        )
        assert services_group_team_id is None

    def test_detach_team_when_services_group_doesnt_exists(self, db_session):
        test_services_group_id = 4
        with pytest.raises(TeamManagerException) as exc:
            TeamManager(db_session).detach_from_services_group(
                services_group_id=test_services_group_id
            )
        assert EXC_SERVICES_GROUP_DOESNT_EXISTS.format(
            test_services_group_id
        ) in str(exc.value)
