from sqlalchemy import exists

from griphook.cli.managers.base import BaseManager
from griphook.cli.managers.exceptions import TeamManagerException
from server.models import ServicesGroup, Team


class TeamManager(BaseManager):
    def create(self, title) -> None:
        if self.session.query(exists().where(Team.title == title)).scalar():
            raise TeamManagerException('Team with the same name already exists')

        self.session.add(Team(title=title))
        self.session.commit()

    def attach_to_service_group(self, service_group_title: str, team_title: str) -> None:
        team = self.session.query(Team).filter_by(title=team_title).scalar()
        if not team:
            raise TeamManagerException('Team with title {} doesn\'t exists'.format(team_title))

        service_group = self.session.query(ServicesGroup).filter_by(title=service_group_title).scalar()
        if not service_group:
            raise TeamManagerException('ServiceGroup with title {} doesn\'t exists'.format(service_group_title))

        service_group.team = team
        self.session.add(service_group)
        self.session.commit()
