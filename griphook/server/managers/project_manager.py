from typing import Optional

from sqlalchemy.sql import exists

from griphook.server.managers.exceptions import ProjectManagerException
from griphook.server.managers.base_manager import BaseManager
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


class ProjectManager(BaseManager):
    def create(self, title: str) -> Project:
        """
        Creates new project instance.
        :param title: project title
        :return: created project instance
        """
        if self.session.query(exists().where(Project.title == title)).scalar():
            raise ProjectManagerException(
                EXC_PROJECT_ALREADY_EXISTS.format(title)
            )
        project = Project(title=title)
        self.session.add(project)
        self.session.commit()
        return project

    def update(self, project_id: int, new_title: str) -> None:
        """
        Updates project instance title.
        :param project_id: project id to update
        :param new_title: new project title to update
        """
        project = self.session.query(Project).filter_by(id=project_id).scalar()
        if not project:
            raise ProjectManagerException(
                EXC_PROJECT_DOESNT_EXISTS.format(project_id)
            )
        project.title = new_title
        self.session.add(project)
        self.session.commit()

    def delete(self, project_id: int) -> None:
        """
        Deletes project instance.
        :param project_id: project id to delete
        """
        project = self.session.query(Project).filter_by(id=project_id).scalar()
        if not project:
            raise ProjectManagerException(
                EXC_PROJECT_DOESNT_EXISTS.format(project_id)
            )
        self.session.delete(project)
        self.session.commit()

    def attach_to_services_group(
        self, project_id: int, services_group_id: int
    ) -> None:
        """
        Attaches project to services group. Also, the method looks
        for all metrics_peaks and metrics_billing with the this
        services group id and attaches the project to them.
        :param project_id: project id to attach
        :param services_group_id: services group id to attach
        """
        self._update_relationship(project_id, services_group_id)

    def detach_from_services_group(self, services_group_id: int) -> None:
        """
        Detaches project from services group. Also, the method looks
        for all metrics_peaks and metrics_billing with the this
        services group id and detaches the project from them.
        :param services_group_id: services group id to detach
        """
        self._update_relationship(None, services_group_id)

    def _update_relationship(
        self, project_id: Optional[int], services_group_id: int
    ) -> None:
        if (
            project_id
            and not self.session.query(
                exists().where(Project.id == project_id)
            ).scalar()
        ):
            raise ProjectManagerException(
                EXC_PROJECT_DOESNT_EXISTS.format(project_id)
            )
        services_group = (
            self.session.query(ServicesGroup)
            .filter_by(id=services_group_id)
            .scalar()
        )
        if not services_group:
            raise ProjectManagerException(
                EXC_SERVICES_GROUP_DOESNT_EXISTS.format(services_group_id)
            )
        services_group.project_id = project_id
        # update relationships for MetricPeak
        metrics_peaks_query = (
            self.session.query(MetricPeak)
            .filter_by(services_group_id=services_group_id)
            .all()
        )
        for metric_peaks in metrics_peaks_query:
            metric_peaks.project_id = project_id
        # update relationships for MetricBilling
        metrics_billing_query = (
            self.session.query(MetricBilling)
            .filter_by(services_group_id=services_group_id)
            .all()
        )
        for metric_billing in metrics_billing_query:
            metric_billing.project_id = project_id

        self.session.add(services_group)
        self.session.add_all(metrics_peaks_query)
        self.session.add_all(metrics_billing_query)
        self.session.commit()
