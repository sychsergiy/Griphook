import datetime

from flask import request, jsonify
from sqlalchemy import func, case

from griphook.server.billing.constants import REQUEST_DATE_TIME_FORMAT
from griphook.server.models import (
    BatchStoryBilling,
    MetricBilling,
    Service,
    ServicesGroup,
)
from griphook.server.billing.utils import get_services_group_metrics_groupe_by_services


def get_billing_metric_values_by_services_group():
    """
        request_json:
        {
            "services_group_id": int,
            "time_from": string,
            "time_until": string
        }

        response_json:
        [
            {
                "service_id": int,
                "service_title": string,
                "cpu": int,
                "memory": int
            }
        ]
    """
    data = request.get_json()
    time_from = datetime.datetime.strptime(
        data.get("time_from"), REQUEST_DATE_TIME_FORMAT
    )
    time_until = datetime.datetime.strptime(
        data.get("time_until"), REQUEST_DATE_TIME_FORMAT
    )
    services_group_id = int(data["services_group_id"])
    # cpu = func.sum(
    #     case(
    #         [(MetricBilling.type == "user_cpu_percent", MetricBilling.value)], else_=0
    #     )
    # ).label("cpu")
    # memory = func.sum(
    #     case([(MetricBilling.type == "vsize", MetricBilling.value)], else_=0)
    # ).label("memory")
    # query = (
    #     MetricBilling.query.join(Service, MetricBilling.service_id == Service.id)
    #     .join(BatchStoryBilling, MetricBilling.batch_id == BatchStoryBilling.id)
    #     .join(ServicesGroup, MetricBilling.services_group_id == ServicesGroup.id)
    #     .filter(BatchStoryBilling.time.between(time_from, time_until))
    #     .filter(ServicesGroup.id == services_group_id)
    #     .with_entities(
    #         cpu,
    #         memory,
    #         Service.title.label("service_title"),
    #         Service.id.label("service_id"),
    #     )
    #     .group_by(Service.id, "service_title")
    #     .order_by(Service.id)
    # )
    metrics = get_services_group_metrics_groupe_by_services(
        services_group_id=services_group_id,
        time_from=time_from,
        time_until=time_until
    )
    resp_data = tuple(
        {
            "cpu": metric.cpu,
            "memory": metric.memory,
            "service_id": metric.service_id,
            "service_title": metric.service_title,
        }
        for metric in metrics
    )
    return jsonify(resp_data)
