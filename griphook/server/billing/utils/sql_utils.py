from sqlalchemy import func, case
from sqlalchemy.sql import label

from griphook.server.models import (MetricBilling, Team, Project, Cluster,
                                    BatchStoryBilling, Service, ServicesGroup, Server)
from griphook.server.billing.utils.formatter import modify_date


def billing_table_query(request_data):
    time_from = modify_date(request_data.get("time_from", None))
    time_until = modify_date(request_data.get("time_until", None))

    cluster_id = request_data.get("cluster_id", None)
    server_id = request_data.get("server_id", None)
    services_groups_ids = request_data.get("services_groups_ids", None)
    project_id = request_data.get("project_id", None)
    team_id = request_data.get("team_id", None)

    query = (
        ServicesGroup.query
        .with_entities(
            label("services_group_title", ServicesGroup.title),
            label("service_group_id", ServicesGroup.id),
            label("team", Team.title),
            label("project", Project.title),
            label("cpu_sum", func.sum(
                case(
                    [(MetricBilling.type == "user_cpu_percent", MetricBilling.value)], else_=0
                )
            )),
            label("memory_sum", func.sum(
                case(
                    [(MetricBilling.type == "vsize", MetricBilling.value)], else_=0
                )
            ))

        )
        .join(MetricBilling, MetricBilling.services_group_id == ServicesGroup.id)
        .join(Team, Team.id == ServicesGroup.team_id)
        .join(Project, Project.id == ServicesGroup.project_id)
        .join(BatchStoryBilling, BatchStoryBilling.id == MetricBilling.batch_id)
        .filter(MetricBilling.type != 'system_cpu_percent')
        .filter(BatchStoryBilling.time.between(time_from, time_until))
        .group_by(
            "services_group_title", "service_group_id", "team", "project"
        )
    )
    if services_groups_ids:
        query = query.filter(ServicesGroup.id.in_(services_groups_ids))
    if team_id:
        query = query.filter(Team.id == team_id)
    if project_id:
        query = query.join(Project, Project.id == ServicesGroup.project_id)
        query = query.filter(Project.id == project_id)
    if server_id or cluster_id:
        query = (
                    query.join(Service, Service.services_group_id == MetricBilling.service_id)
                         .join(Server, Service.server_id == Server.id)
                 )
        if server_id:
            query = query.filter(Server.id == server_id)
        if cluster_id:
            query = query.join(Cluster, Cluster.id == Server.cluster_id)
            query = query.filter(Cluster.id == cluster_id)

    result = query.all()
    return result










