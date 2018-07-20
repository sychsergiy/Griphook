from griphook.cli.managers.base import BaseManager
from griphook.cli.managers.exceptions import ProjectManagerException
from griphook.db.models import Project, ServicesGroup


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
