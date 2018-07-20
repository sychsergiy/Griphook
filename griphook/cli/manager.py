from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from griphook.config.config import Config
from griphook.db.models import Team, Project, ServicesGroup


def get_session_class():
    config = Config()
    db_url = config.options["db"]["DATABASE_URL"]
    engine = create_engine(db_url)
    return sessionmaker(bind=engine)


Session = get_session_class()


class ManagerException(Exception):
    pass


# todo: remote __del__ method
# todo:  divide manager to different classes (TeamManager(BaseManager), ProjectManager(BaseManager), FilterManager)
class Manager(object):
    def __init__(self, session):
        self.session = session

    def __del__(self):
        self.session.close()

    def create_team(self, title) -> None:
        team = self.session.query(Team).filter_by(title=title).first()
        if team:
            raise ManagerException('Team with the same name already exists')

        instance = Team(title=title)
        self.session.add(instance)
        self.session.commit()

    def create_project(self, title) -> None:
        team = self.session.query(Project).filter_by(title=title).first()
        if team:
            raise ManagerException('Project with the same name already exists')

        instance = Project(title=title)
        self.session.add(instance)
        self.session.commit()

    def attach_service_group_to_project(self, service_group_title: str, project_title: str) -> None:
        project = self.session.query(Project).filter_by(title=project_title).first()
        if not project:
            raise ManagerException('Project with title {} doesn\'t exists'.format(project_title))

        service_group = self.session.query(ServicesGroup).filter_by(title=service_group_title).first()
        if not service_group:
            raise ManagerException('ServiceGroup with title {} doesn\'t exists'.format(service_group_title))

        service_group.project = project
        self.session.add(service_group)
        self.session.commit()

    def attach_service_group_to_team(self, service_group_title: str, team_title: str) -> None:
        team = self.session.query(Team).filter_by(title=team_title).first()
        if not team:
            raise ManagerException('Team with title {} doesn\'t exists'.format(team_title))

        service_group = self.session.query(ServicesGroup).filter_by(title=service_group_title).first()
        if not service_group:
            raise ManagerException('ServiceGroup with title {} doesn\'t exists'.format(service_group_title))

        service_group.team = team
        self.session.add(service_group)
        self.session.commit()
