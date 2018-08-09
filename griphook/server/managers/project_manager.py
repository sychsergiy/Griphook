from sqlalchemy.sql import exists

from griphook.server.models import Metric, Project, ServicesGroup
from griphook.server.managers.exceptions import ProjectManagerException
from griphook.server.managers.base_manager import BaseManager
from griphook.server.managers.constants import (
    EXC_SERVICES_GROUP_DOESNT_EXISTS,
    EXC_PROJECT_ALREADY_EXISTS,
    EXC_PROJECT_DOESNT_EXISTS
)


class ProjectManager(BaseManager):
    def create(self, title):
        if self.session.query(exists().where(Project.title == title)).scalar():
            raise ProjectManagerException(EXC_PROJECT_ALREADY_EXISTS.format(title))

        self.session.add(Project(title=title))
        self.session.commit()

    def update(self, project_id, new_title):
        project = self.session.query(Project).filter_by(id=project_id).scalar()
        if not project:
            raise ProjectManagerException(EXC_PROJECT_DOESNT_EXISTS.format(project_id))

        project.title = new_title
        self.session.add(project)
        self.session.commit()

    def delete(self, project_id):
        project = self.session.query(Project).filter_by(id=project_id).scalar()
        if not project:
            raise ProjectManagerException(EXC_PROJECT_DOESNT_EXISTS.format(project_id))

        self.session.delete(project)
        self.session.commit()

    def attach_to_services_group(self, project_id, services_group_id):
        self._update_relationship(project_id, services_group_id)

    def detach_from_services_group(self, services_group_id):
        self._update_relationship(None, services_group_id)

    def _update_relationship(self, project_id, services_group_id):
        if project_id and not self.session.query(exists().where(Project.id == project_id)).scalar():
            raise ProjectManagerException(EXC_PROJECT_DOESNT_EXISTS.format(project_id))

        services_group = self.session.query(ServicesGroup).filter_by(id=services_group_id).scalar()
        if not services_group:
            raise ProjectManagerException(EXC_SERVICES_GROUP_DOESNT_EXISTS.format(services_group_id))
        services_group.project_id = project_id

        metrics = self.session.query(Metric).filter_by(services_group_id=services_group_id).all()
        for metric in metrics:
            metric.project_id = project_id

        self.session.add(services_group, metrics)
        self.session.commit()
