from griphook.cli.utils.db_utils import get_session_class
from griphook.db.models import Team, Project, ServicesGroup

from griphook.cli.managers.exceptions import ProjectManagerException, TeamManagerException

Session = get_session_class()


class BaseManager(object):
    def __init__(self, session):
        self.session = session


class ProjectManager(BaseManager):
    def create(self, title) -> None:
        project = self.session.query(Project).filter_by(title=title).first()
        if project:
            raise ProjectManagerException('Project with the same name already exists')

        instance = Project(title=title)
        self.session.add(instance)
        self.session.commit()

    def attach_to_service_group(self, service_group_title: str, project_title: str) -> None:
        project = self.session.query(Project).filter_by(title=project_title).first()
        if not project:
            raise ProjectManagerException('Project with title {} doesn\'t exists'.format(project_title))

        service_group = self.session.query(ServicesGroup).filter_by(title=service_group_title).first()
        if not service_group:
            raise ProjectManagerException('ServiceGroup with title {} doesn\'t exists'.format(service_group_title))

        service_group.project = project
        self.session.add(service_group)
        self.session.commit()


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
