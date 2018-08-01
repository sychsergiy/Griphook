import json

import requests

from typing import Iterable, Tuple

from griphook.api.graphite.target import MultipleValues, DotPath
from griphook.server.models import Service

from griphook.server.average_load.graphite import average, summarize, send_graphite_request


def get_average_services_load_chart_data(service: str, time_from: int, time_until: int,
                                         metric_type: str, server='*', service_group='*'):
    services = (
        Service.query
            .filter(Service.title == service).distinct()
            .with_entities(Service.instance)
    ).all()
    instances = tuple(instance for (instance,) in services)
    # todo: calc with server and service_group arguments if they are given

    # todo: important to take services form each service_group separate

    path_to_instances = f'{service_group}:{service}'
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
    complex_target = list(complex_target_generator(service, instances, metric_type))
    params = {
        'format': 'json',
        'target': complex_target,
        'from': str(time_from),
        'until': str(time_until),
    }
    instances_average_response = send_graphite_request(params=params)

    service_average_response_json = json.loads(service_average_response)
    instances_average_response_json = json.loads(instances_average_response)

    response_data = construct_response_for_server_api_view(service_average_response_json,
                                                           instances_average_response_json,
                                                           service, instances, metric_type)
    return response_data


def complex_target_generator(service, instances: Iterable[str], metric_type: str,
                             server: str = '*', service_group: str = '*'):
    for instance in instances:
        path_to_instances = DotPath('cantal', '*', f'{server}', 'cgroups', 'lithos',
                                    f'{service_group}:{service}', f'{instance}')

        path_with_metric = str(path_to_instances + metric_type)

        yield average(summarize(path_with_metric, "3month", 'avg'))


def construct_response_for_server_api_view(parent_json: tuple, children_json: dict, service: str,
                                           children_title_order: Tuple[str],
                                           metric_type: str, server: str = '*', service_group: str = '*'):
    # todo: use target prefix
    service_target = f'cantal.*.{server}.cgroups.lithos.{service_group}:{service}'
    service_target_value = parent_json[0]['datapoints'][0][0]

    def response_children_generator():
        for index, value in enumerate(children_json):
            # graphite returns seriesLists in the same order like targets was given
            # so it is possible just to take service_group_title from services_groups_list with the same index
            instance = children_title_order[index]
            # todo: target must be constructed with parameters, depends on view(server, sv_group, service)
            path = DotPath('cantal', '*', f'{server}', 'cgroups', 'lithos', f'{service_group}:{service}', f'{instance}')
            target = str(path + metric_type)
            yield {
                'target': target,
                'value': value['datapoints'][0][0],
            }

    result = {
        'root': {
            'target': service_target,
            'value': service_target_value
        },
        'children': list(response_children_generator())
    }
    return result
