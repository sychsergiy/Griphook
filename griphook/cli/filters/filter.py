from sqlalchemy.orm import Query

from server.models import Project, ServicesGroup, Team


class ServiceGroupFilter(object):
    def __init__(self, session, query: Query = None) -> None:
        self.session = session
        self.query = query if query else self.session.query(ServicesGroup)

        self.team_joined = False
        self.project_joined = False

    def filter_by_titles(self, *args: str):
        self.query = self.query.filter(ServicesGroup.title.in_(args))
        return self

    def filter_by_team_titles(self, *args: str):
        if not self.team_joined:
            self.query = self.query.join(Team)
            self.team_joined = True
        self.query = self.query.filter(Team.title.in_(args))
        return self

    def filter_by_project_titles(self, *args: str):
        if not self.project_joined:
            self.query = self.query.join(Project)
            self.project_joined = True
        self.query = self.query.filter(Project.title.in_(args))
        return self

    def items(self) -> list:
        return self.query.all()
