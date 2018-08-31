from datetime import timedelta

from flask import current_app as app
from sqlalchemy import func, case
from sqlalchemy.sql import column, and_

from griphook.server.models import (
    db,
    MetricBilling,
    Team,
    Project,
    BatchStoryBilling,
    Service,
    ServicesGroup,
    Server,
    Cluster,
)

from griphook.server.billing.constants import ALLOWED_METRIC_TYPES

# Max number of points will be returned by `get_services_group_data_chart`
MAX_POINTS = 1000


def case_builder(metrics_type, coef):
    condition = MetricBilling.type == metrics_type
    return func.avg(case([(condition, MetricBilling.value * coef)], else_=0))


def get_time_coef(time_from, time_until):
    return (time_until - time_from).days / 30


def get_billing_table_data(filters):
    time_from = filters.get("time_from")
    time_until = filters.get("time_until")
    target_type = filters.get("target_type")
    target_ids = filters.get("target_ids")
    page = filters.get("page")
    metrics_per_page = app.config["BILLING_TABLE_METRICS_PER_PAGE"]

    # todo: add filster by projects, teams, clusters

    time_coef = get_time_coef(time_from, time_until)
    memory_coef = 1.5 * time_coef / 10 ** 9
    cpu_coef = 9 * time_coef / 100

    memory_result = get_services_groups_resources(
        "vsize", time_from, time_until, memory_coef, target_type, target_ids
    ).subquery()

    cpu_result = get_services_groups_resources(
        "user_cpu_percent",
        time_from,
        time_until,
        cpu_coef,
        target_type,
        target_ids,
    ).subquery()

    result_query = db.session.query(
        memory_result.c.title,
        memory_result.c.services_group_id,
        memory_result.c.team,
        memory_result.c.project,
        memory_result.c.metric_sum,
        cpu_result.c.metric_sum,
    ).join(
        cpu_result,
        cpu_result.c.services_group_id == memory_result.c.services_group_id,
    )
    return result_query.paginate(per_page=metrics_per_page, page=page)


def get_services_group_data_group_by_services(
        services_group_id, time_from, time_until
):
    cpu = case_builder(ALLOWED_METRIC_TYPES.get("user_cpu_percent"), 100).label(
        "cpu"
    )
    memory = case_builder(ALLOWED_METRIC_TYPES.get("vsize"), 1 / 10 ** 9).label("memory")
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
            .group_by(Service.id, Service.title)
            .order_by(Service.id)
    )
    return query.all()


def get_services_group_data_chart(
        services_group_id, time_from, time_until, metric_type
):
    """
    Return data for billing cpu/vsize charts.
    If for time_from-time_until period number of data points more then
    `MAX_POINTS`, data will be aggregated to get less number of points.
    """
    delta = time_until - time_from
    # Compute interval (in hours) for grouping data, it can't be 0
    interval = delta.total_seconds() // (3600 * MAX_POINTS) or 1

    serie = db.session.query(
        func.generate_series(
            time_from, time_until, timedelta(hours=interval)
        ).label("date")
    ).subquery()

    metrics = (
        db.session.query(
            serie.c.date.label("time"),
            serie.c.date + timedelta(hours=interval),
            func.coalesce(func.avg(column("value")), 0).label("value"),
        )
            .outerjoin(
            BatchStoryBilling,
            and_(
                BatchStoryBilling.time >= serie.c.date,
                BatchStoryBilling.time
                < (serie.c.date + timedelta(hours=interval)),
            ),
        )
            .outerjoin(
            MetricBilling,
            and_(
                MetricBilling.batch_id == BatchStoryBilling.id,
                MetricBilling.type == metric_type,
                MetricBilling.services_group_id == services_group_id,
            ),
        )
            .group_by(serie.c.date)
            .order_by(serie.c.date)
    )

    return metrics.all()


def get_services_groups_resources(
        metric_type, time_from, time_until, coefficient, target_type, target_ids
):
    """Return services_groups resources for `metric_type`"""
    services_average_values = (
        db.session.query(
            MetricBilling.service_id.label("service_id"),
            func.avg(MetricBilling.value).label("value"),
        )
            .join(BatchStoryBilling, BatchStoryBilling.id == MetricBilling.batch_id)
            .filter(MetricBilling.type == metric_type)
            .filter(BatchStoryBilling.time.between(time_from, time_until))
            .group_by(MetricBilling.service_id)
    ).subquery()

    services_groups_resources = (
        db.session.query(
            ServicesGroup.title.label("title"),
            ServicesGroup.id.label("services_group_id"),
            Team.title.label("team"),
            Project.title.label("project"),
            func.sum(services_average_values.c.value * coefficient).label(
                "metric_sum"
            ),
        )
            .join(Service, Service.services_group_id == ServicesGroup.id)
            .join(
            services_average_values,
            Service.id == services_average_values.c.service_id,
        )
            .outerjoin(Team, Team.id == ServicesGroup.team_id)
            .outerjoin(Project, Project.id == ServicesGroup.project_id)
            .group_by(
            ServicesGroup.id, ServicesGroup.title, Project.title, Team.title
        )
    )

    if target_type == "team":
        services_groups_resources = services_groups_resources.filter(
            Team.id.in_(target_ids)
        )
    elif target_type == "project":
        services_groups_resources = services_groups_resources.filter(
            Project.id.in_(target_ids)
        )
    elif target_type == "server":
        services_groups_resources = services_groups_resources.join(
            Server, Server.id == Service.server_id
        ).filter(Server.id.in_(target_ids))
    elif target_type == "cluster":
        services_groups_resources = (
            services_groups_resources.join(
                Server, Server.id == Service.server_id
            )
                .join(Cluster, Cluster.id == Server.cluster_id)
                .filter(Cluster.id.in_(target_ids))
        )
    elif target_type == "services_group":
        services_groups_resources = services_groups_resources.filter(
            ServicesGroup.id.in_(target_ids)
        )
    return services_groups_resources
