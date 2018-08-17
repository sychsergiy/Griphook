from cerberus import Validator
from sqlalchemy import case, func

from griphook.server.billing.common import string_to_date_time
from griphook.server.billing.constants import RESPONSE_DATE_TIME_FORMAT
from griphook.server.models import (
    MetricBilling,
    BatchStoryBilling,
    Service,
    ServicesGroup,
)


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


def validate_data_for_general_table_metrics(validation_data):
    schema = {
        "services_group_id": {"type": "integer", "required": True},
        "time_from": {
            "type": "date",
            "required": True,
            "coerce": string_to_date_time,
        },
        "time_until": {
            "type": "date",
            "required": True,
            "coerce": string_to_date_time,
        },
    }
    v = Validator()
    is_valid = v.validate(validation_data, schema)
    return is_valid, v.errors, v.document


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


def format_metrics_list_to_chart(metrics):
    chart = {"timeline": [], "values": []}
    for metric in metrics:
        chart["timeline"].append(
            metric.time.strftime(RESPONSE_DATE_TIME_FORMAT)
        )
        chart["values"].append(round(metric.value, 1))
    return chart
