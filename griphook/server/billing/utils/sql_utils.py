from sqlalchemy import func, case
from sqlalchemy.sql import label

from griphook.server.models import (MetricBilling, Team, Project, Cluster,
                                    BatchStoryBilling, Service, ServicesGroup, Server)


def billing_table_query(data):
    time_from = data.get("time_from")
    time_until = data.get("time_until")
    target_type = data.get("target_type")
    target_ids = data.get("target_ids")
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
    if target_type == "all":
        return query.all()
    elif target_type == "services_groups":
        query = query.filter(ServicesGroup.id.in_(target_ids))
    elif target_type == "team":
        query = query.filter(Team.id.in_(target_ids))
    elif target_type == "project":
        query = query.join(Project, Project.id == ServicesGroup.project_id)
        query = query.filter(Project.id.id_(target_ids))
    elif target_type == "server" or target_type == "cluster":
        query = (
            query.join(Service, Service.services_group_id == MetricBilling.service_id)
                 .join(Server, Service.server_id == Server.id)
        )
        if target_type == "server":
            query = query.filter(Server.id.in_(target_ids))
        else:
            query = query.join(Cluster, Cluster.id == Server.cluster_id)
            query = query.filter(Cluster.id.in_(target_ids))
    result = query.all()
    return result
