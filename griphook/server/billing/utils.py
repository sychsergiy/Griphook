from datetime import datetime

from sqlalchemy import func, case
from sqlalchemy.sql import label
from cerberus import Validator

from griphook.server.models import (MetricBilling, Team, Project, Cluster,
                                    BatchStoryBilling, Service, ServicesGroup, Server)


def is_correct_time_format(raw_date) -> bool:
    try:
        modify_date(raw_date, "%Y-%m-%d")
    except ValueError:
        return False
    except TypeError:
        return False

    return True


def modify_date(date):
    return datetime.strptime(date, "%Y-%m-%d")


def output_formatter(row):
    return row.service_group, row.cpu, row.memory


def is_valid_date_format(request_json: dict) -> bool:
    is_valid_time_from = is_correct_time_format(request_json.get("time_from", None))
    is_valid_time_until = is_correct_time_format(request_json.get("time_until", None))
    return is_valid_time_from and is_valid_time_until


def validate_request_json(schema: dict, request_json: dict) -> (bool, dict):
    v = Validator(schema)
    return not (v.validate(request_json) and is_valid_date_format(request_json)), v.errors


def billing_table_query(request_data):
    time_from = modify_date(request_data.get("time_from", None))
    time_until = modify_date(request_data.get("time_until", None))

    cluster_id = request_data.get("cluster_id", None)
    server_id = request_data.get("server_id", None)
    services_groups_ids = request_data.get("services_groups", None)
    project_id = request_data.get("project_id", None)
    team_id = request_data.get("team_id", None)

    query = (
        ServicesGroup.query
        .with_entities(
            label("service_group", ServicesGroup.title),
            label("service_group_id", ServicesGroup.id),
            label("team", Team.title),
            label("project", Project.title),
            label("cpu", func.sum(
                case(
                    [(MetricBilling.type == "user_cpu_percent", MetricBilling.value)], else_=0
                )
            )),
            label("memory", func.sum(
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
            "service_group", "service_group_id", "team", "project"
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










