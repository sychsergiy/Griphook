from griphook.cli.managers.base import BaseManager
from griphook.cli.managers.exceptions import TeamManagerException
from griphook.db.models import Team, ServicesGroup


class TeamManager(BaseManager):

    def create(self, title) -> None:
        team = self.session.query(Team).filter_by(title=title).first()
        if team:
            raise TeamManagerException('Team with the same name already exists')

        instance = Team(title=title)
        self.session.add(instance)
        self.session.commit()

    def attach_to_service_group(self, service_group_title: str, team_title: str) -> None:
        team = self.session.query(Team).filter_by(title=team_title).first()
        if not team:
            raise TeamManagerException('Team with title {} doesn\'t exists'.format(team_title))

        service_group = self.session.query(ServicesGroup).filter_by(title=service_group_title).first()
        if not service_group:
            raise TeamManagerException('ServiceGroup with title {} doesn\'t exists'.format(service_group_title))

        service_group.team = team
        self.session.add(service_group)
        self.session.commit()
