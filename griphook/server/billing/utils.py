from sqlalchemy import case, func

from griphook.server.models import MetricBilling, BatchStoryBilling, Service, ServicesGroup


def get_services_group_metrics_groupe_by_services(services_group_id, time_from, time_until):
    cpu = func.sum(
        case(
            [(MetricBilling.type == "user_cpu_percent", MetricBilling.value)], else_=0
        )
    ).label("cpu")
    memory = func.sum(
        case([(MetricBilling.type == "vsize", MetricBilling.value)], else_=0)
    ).label("memory")
    query = (
        MetricBilling.query
        .join(Service, MetricBilling.service_id == Service.id)
        .join(BatchStoryBilling, MetricBilling.batch_id == BatchStoryBilling.id)
        .join(ServicesGroup, MetricBilling.services_group_id == ServicesGroup.id)
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