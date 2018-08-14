from sqlalchemy.sql import exists

from griphook.server.models import MetricPeak, Team, ServicesGroup
from griphook.server.managers.exceptions import TeamManagerException
from griphook.server.managers.base_manager import BaseManager
from griphook.server.managers.constants import (
    EXC_SERVICES_GROUP_DOESNT_EXISTS,
    EXC_TEAM_ALREADY_EXISTS,
    EXC_TEAM_DOESNT_EXISTS,
)


class TeamManager(BaseManager):
    def create(self, title):
        if self.session.query(exists().where(Team.title == title)).scalar():
            raise TeamManagerException(EXC_TEAM_ALREADY_EXISTS.format(title))
        team = Team(title=title)
        self.session.add(team)
        self.session.commit()
        return team

    def update(self, team_id, new_title):
        team = self.session.query(Team).filter_by(id=team_id).scalar()
        if not team:
            raise TeamManagerException(EXC_TEAM_DOESNT_EXISTS.format(team_id))
        team.title = new_title
        self.session.add(team)
        self.session.commit()

    def delete(self, team_id):
        team = self.session.query(Team).filter_by(id=team_id).scalar()
        if not team:
            raise TeamManagerException(EXC_TEAM_DOESNT_EXISTS.format(team_id))
        self.session.delete(team)
        self.session.commit()

    def attach_to_services_group(self, team_id, services_group_id):
        self._update_relationship(team_id, services_group_id)

    def detach_from_services_group(self, services_group_id):
        self._update_relationship(None, services_group_id)

    def _update_relationship(self, team_id, services_group_id):
        if (
            team_id
            and not self.session.query(
                exists().where(Team.id == team_id)
            ).scalar()
        ):
            raise TeamManagerException(EXC_TEAM_DOESNT_EXISTS.format(team_id))
        services_group = (
            self.session.query(ServicesGroup)
            .filter_by(id=services_group_id)
            .scalar()
        )

        if not services_group:
            raise TeamManagerException(
                EXC_SERVICES_GROUP_DOESNT_EXISTS.format(services_group_id)
            )
        services_group.team_id = team_id

        metrics = (
            self.session.query(MetricPeak)
            .filter_by(services_group_id=services_group_id)
            .all()
        )

        for metric in metrics:
            metric.team_id = team_id

        self.session.add(services_group, metrics)
        self.session.commit()
