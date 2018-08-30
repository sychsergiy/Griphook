from datetime import timedelta

from flask import current_app as app
from sqlalchemy import func, case
from sqlalchemy.sql import label, func, column, and_

from griphook.server.models import (
    db,
    MetricBilling,
    Team,
    Project,
    Cluster,
    BatchStoryBilling,
    Service,
    ServicesGroup,
    Server,
)

from griphook.server.billing.constants import (
    ALLOWED_TARGET_TYPES,
    ALLOWED_METRIC_TYPES,
)


def case_builder(metrics_type):
    condition = MetricBilling.type == metrics_type
    return func.sum(case([(condition, MetricBilling.value)], else_=0))


def get_billing_table_data(filters):
    time_from = filters.get("time_from")
    time_until = filters.get("time_until")
    target_type = filters.get("target_type")
    target_ids = filters.get("target_ids")
    page = filters.get("page")
    metrics_per_page = app.config["BILLING_TABLE_METRICS_PER_PAGE"]
    # TODO create left join for services_groups with team and project
    query = (
        ServicesGroup.query.with_entities(
            label("services_group_title", ServicesGroup.title),
            label("service_group_id", ServicesGroup.id),
            label("team", Team.title),
            label("project", Project.title),
            label(
                "cpu_sum",
                case_builder(ALLOWED_METRIC_TYPES.get("user_cpu_percent")),
            ),
            label(
                "memory_sum", case_builder(ALLOWED_METRIC_TYPES.get("vsize"))
            ),
        )
        .join(
            MetricBilling, MetricBilling.services_group_id == ServicesGroup.id
        )
        .outerjoin(Team, Team.id == ServicesGroup.team_id)
        .outerjoin(Project, Project.id == ServicesGroup.project_id)
        .join(BatchStoryBilling, BatchStoryBilling.id == MetricBilling.batch_id)
        .filter(
            MetricBilling.type != ALLOWED_METRIC_TYPES.get("system_cpu_percent")
        )
        .filter(BatchStoryBilling.time.between(time_from, time_until))
        .group_by("services_group_title", "service_group_id", "team", "project")
    )
    if target_type == ALLOWED_TARGET_TYPES.get("all"):
        pass
    elif target_type == ALLOWED_TARGET_TYPES.get("services_group"):
        query = query.filter(ServicesGroup.id.in_(target_ids))
    elif target_type == ALLOWED_TARGET_TYPES.get("team"):
        query = query.filter(Team.id.in_(target_ids))
    elif target_type == ALLOWED_TARGET_TYPES.get("project"):
        query = query.filter(Project.id.in_(target_ids))
    elif target_type == ALLOWED_TARGET_TYPES.get(
        "server"
    ) or target_type == ALLOWED_TARGET_TYPES.get("cluster"):
        query = query.join(
            Service, Service.id == MetricBilling.service_id
        ).join(Server, Service.server_id == Server.id)
        if target_type == ALLOWED_TARGET_TYPES.get("server"):
            query = query.filter(Server.id.in_(target_ids))
        elif target_type == ALLOWED_TARGET_TYPES.get("cluster"):
            query = query.join(Cluster, Cluster.id == Server.cluster_id)
            query = query.filter(Cluster.id.in_(target_ids))
    result = query.paginate(per_page=metrics_per_page, page=page)
    return result


def get_services_group_data_group_by_services(
    services_group_id, time_from, time_until
):
    cpu = case_builder(ALLOWED_METRIC_TYPES.get("user_cpu_percent")).label("cpu")
    memory = case_builder(ALLOWED_METRIC_TYPES.get("vsize")).label("memory")
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


def get_services_group_data_chart(
    services_group_id, time_from, time_until, metric_type
):
    MAX_POINTS = 1000

    delta = time_until - time_from
    # Compute interval (in hours) for grouping data, it can't be 0
    interval = delta.total_seconds() // (3600 * MAX_POINTS) or 1

    serie = (
        db.session
        .query(
            func.generate_series(
                time_from,
                time_until,
                timedelta(hours=interval)
            ).label('date')
        ).subquery()
    )

    metrics = (
        db.session
        .query(
            serie.c.date.label('time'),
            serie.c.date + timedelta(hours=interval),
            func.coalesce(func.avg(column('value')), 0).label('value')
        )
        .outerjoin(
            BatchStoryBilling, 
            and_(BatchStoryBilling.time >= serie.c.date,
                 BatchStoryBilling.time < (serie.c.date + timedelta(hours=2)))
        )
        .outerjoin(
            MetricBilling,
            and_(MetricBilling.batch_id == BatchStoryBilling.id,
                 MetricBilling.type == metric_type,
                 MetricBilling.services_group_id == services_group_id)
        )
        .group_by(serie.c.date)
        .order_by(serie.c.date)
    )

    return metrics.all()



