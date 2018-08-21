from typing import Optional

from sqlalchemy.sql import exists

from griphook.server.managers.exceptions import TeamManagerException
from griphook.server.managers.base_manager import BaseManager
from griphook.server.managers.constants import (
    EXC_SERVICES_GROUP_DOESNT_EXISTS,
    EXC_TEAM_ALREADY_EXISTS,
    EXC_TEAM_DOESNT_EXISTS,
)
from griphook.server.models import (
    ServicesGroup,
    MetricBilling,
    MetricPeak,
    Team,
)


class TeamManager(BaseManager):
    def create(self, title: str) -> Team:
        """
        Creates new team instance.
        :param title: team title
        :return: created team instance
        """
        if self.session.query(exists().where(Team.title == title)).scalar():
            raise TeamManagerException(EXC_TEAM_ALREADY_EXISTS.format(title))
        team = Team(title=title)
        self.session.add(team)
        self.session.commit()
        return team

    def update(self, team_id: int, new_title: str) -> None:
        """
        Updates team instance title.
        :param team_id: team id to update
        :param new_title: new team title to update
        """
        team = self.session.query(Team).filter_by(id=team_id).scalar()
        if not team:
            raise TeamManagerException(EXC_TEAM_DOESNT_EXISTS.format(team_id))
        team.title = new_title
        self.session.add(team)
        self.session.commit()

    def delete(self, team_id: int) -> None:
        """
        Deletes team instance.
        :param team_id: team id to delete
        """
        team = self.session.query(Team).filter_by(id=team_id).scalar()
        if not team:
            raise TeamManagerException(EXC_TEAM_DOESNT_EXISTS.format(team_id))
        self.session.delete(team)
        self.session.commit()

    def attach_to_services_group(
        self, team_id: int, services_group_id: int
    ) -> None:
        """
        Attaches team to services group. Also, the method looks
        for all metrics_peaks and metrics_billing with the this
        services group id and attaches the team to them.
        :param team_id: team id to attach
        :param services_group_id: services group id to attach
        """
        self._update_relationship(team_id, services_group_id)

    def detach_from_services_group(self, services_group_id: int) -> None:
        """
        Detaches team from services group. Also, the method looks
        for all metrics_peaks and metrics_billing with the this
        services group id and detaches the team from them.
        :param services_group_id: services group id to detach
        """
        self._update_relationship(None, services_group_id)

    def _update_relationship(
        self, team_id: Optional[int], services_group_id: int
    ) -> None:
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
        # update relationships for MetricPeak
        metrics_peaks_query = (
            self.session.query(MetricPeak)
            .filter_by(services_group_id=services_group_id)
            .all()
        )
        for metric_peaks in metrics_peaks_query:
            metric_peaks.team_id = team_id
        # update relationships for MetricBilling
        metrics_billing_query = (
            self.session.query(MetricBilling)
            .filter_by(services_group_id=services_group_id)
            .all()
        )
        for metric_billing in metrics_billing_query:
            metric_billing.team_id = team_id

        self.session.add(services_group)
        self.session.add_all(metrics_peaks_query)
        self.session.add_all(metrics_billing_query)
        self.session.commit()
