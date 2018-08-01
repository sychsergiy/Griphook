import json

from typing import Iterable

from griphook.api.graphite.target import MultipleValues, DotPath
from griphook.server.models import Service

from griphook.server.average_load.graphite import average, summarize, send_graphite_request
from griphook.server.average_load.response import construct_response_for_services_api_view, \
    complex_services_target_generator


def get_average_services_load_chart_data(service: str, time_from: int, time_until: int,
                                         metric_type: str, server='*', services_group='*'):
    services = (
        Service.query
            .filter(Service.title == service).distinct()
            .with_entities(Service.instance)
    ).all()
    instances = tuple(instance for (instance,) in services)
    # todo: calc with server and service_group arguments if they are given

    # todo: important to take services form each service_group separate

    path_to_instances = f'{services_group}:{service}'
    target_instances = MultipleValues(*instances)
    # todo: do I really need to insert instances here or just take all from service

    path_to_instances = DotPath('cantal', '*', f'{server}', 'cgroups', 'lithos', f'{path_to_instances}',
                                f'{target_instances}', )
    path_with_metric = str(path_to_instances + metric_type)

    full_target = average(summarize(path_with_metric, "3month", 'avg'))

    params = {
        'format': 'json',
        'target': full_target,
        'from': str(time_from),
        'until': str(time_until),
    }
    service_average_response = send_graphite_request(params)  # get average value for server

    # ------------------------------
    complex_target = list(complex_services_target_generator(service, instances, metric_type))
    params = {
        'format': 'json',
        'target': complex_target,
        'from': str(time_from),
        'until': str(time_until),
    }
    instances_average_response = send_graphite_request(params=params)

    service_average_response_json = json.loads(service_average_response)
    instances_average_response_json = json.loads(instances_average_response)

    target = f'cantal.*.{server}.cgroups.lithos.{services_group}:{service}'
    response_data = construct_response_for_services_api_view(
        target, service_average_response_json, instances_average_response_json,
        instances, metric_type, service=service
    )
    return response_data
