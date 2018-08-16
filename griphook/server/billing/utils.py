from datetime import datetime

from cerberus import Validator
from sqlalchemy import case, func

from griphook.server.models import (
    MetricBilling,
    BatchStoryBilling,
    Service,
    ServicesGroup,
)
from griphook.server.billing.constants import REQUEST_DATE_TIME_FORMAT


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
    time_formatter = lambda t: datetime.strptime(t, REQUEST_DATE_TIME_FORMAT)
    schema = {
        "services_group_id": {"type": "integer", "required": True},
        "time_from": {
            "type": "datetime",
            "required": True,
            "coerce": time_formatter,
        },
        "time_until": {
            "type": "datetime",
            "required": True,
            "coerce": time_formatter,
        },
    }
    v = Validator()
    is_valid = v.validate(validation_data, schema)
    return is_valid, v.errors, v.document
