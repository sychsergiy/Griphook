from sqlalchemy import func, case
from sqlalchemy.sql import label

from griphook.server.models import (MetricBilling, Team, Project, Cluster,
                                    BatchStoryBilling, Service, ServicesGroup, Server)


def billing_table_query(data):
    time_from = data.get("time_from")
    time_until = data.get("time_until")
    target_type = data.get("target_type")
    target_ids = data.get("target_ids")
    # TODO create left join for services_groups with team and project
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
        .outerjoin(Team, Team.id == ServicesGroup.team_id)
        .outerjoin(Project, Project.id == ServicesGroup.project_id)
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


def get_services_group_metrics_group_by_services(
    services_group_id, time_from, time_until
):
    cpu = func.sum(
        case(
            [(MetricBilling.type == "user_cpu_percent", MetricBilling.value)],
            else_=0,
        )
    ).label("cpu")
    memory = func.sum(
        case([(MetricBilling.type == "vsize", MetricBilling.value)], else_=0)
    ).label("memory")
    query = (
        MetricBilling.query.join(
            Service, MetricBilling.service_id == Service.id
        )
        .join(BatchStoryBilling, MetricBilling.batch_id == BatchStoryBilling.id)
        .join(
            ServicesGroup, MetricBilling.services_group_id == ServicesGroup.id
        )
        .filter(BatchStoryBilling.time.between(time_from, time_until))
        .filter(ServicesGroup.id == services_group_id)
        .with_entities(
            cpu,
            memory,
            Service.title.label("service_title"),
            Service.id.label("service_id"),
        )
        .group_by(Service.id, "service_title")
        .order_by(Service.id)
    )
    return query.all()


def get_services_group_metrics_chart(
    services_group_id, time_from, time_until, metric_type
):
    query = (
        MetricBilling.query.join(
            Service, MetricBilling.service_id == Service.id
        )
        .join(BatchStoryBilling, MetricBilling.batch_id == BatchStoryBilling.id)
        .join(
            ServicesGroup, MetricBilling.services_group_id == ServicesGroup.id
        )
        .filter(BatchStoryBilling.time.between(time_from, time_until))
        .filter(ServicesGroup.id == services_group_id)
        .filter(MetricBilling.type == metric_type)
        .with_entities(
            MetricBilling.value.label("value"),
            BatchStoryBilling.time.label("time"),
        )
        .order_by(BatchStoryBilling.time)
    )
    return query.all()
