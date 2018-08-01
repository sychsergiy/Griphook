from typing import Iterable

from griphook.api.graphite.target import DotPath
from griphook.server.average_load.graphite import average, summarize


def construct_target(metric_type, server='*', services_group='*', service='*', instance='*'):
    path = DotPath('cantal', '*', f'{server}', 'cgroups', 'lithos', f'{services_group}:{service}', f'{instance}')
    return str(path + metric_type)


def construct_response_for_services_groups_api_view(target: str, parent_json: tuple, children_json: dict,
                                                    children_title_order: tuple, metric_type: str, services_group: str,
                                                    server: str = '*'):
    service_group_target_value = parent_json[0]['datapoints'][0][0]

    def response_children_generator():
        for index, value in enumerate(children_json):
            # graphite returns seriesLists in the same order like targets was given
            # so it is possible just to take service_group_title from services_groups_list with the same index
            service = children_title_order[index]
            yield {
                'target': construct_target(metric_type, server, services_group, service),
                'value': value['datapoints'][0][0],
            }

    result = {
        'root': {
            'target': target,
            'value': service_group_target_value
        },
        'children': list(response_children_generator())
    }
    return result


def construct_response_for_services_api_view(target: str, parent_json: tuple, children_json: dict,
                                             children_title_order: tuple,
                                             metric_type: str, service: str, server: str = '*',
                                             services_group: str = '*'):
    service_target_value = parent_json[0]['datapoints'][0][0]

    def response_children_generator():
        for index, value in enumerate(children_json):
            # graphite returns seriesLists in the same order like targets was given
            # so it is possible just to take service_group_title from services_groups_list with the same index
            instance = children_title_order[index]
            yield {
                'target': construct_target(metric_type, server, services_group, service, instance),
                'value': value['datapoints'][0][0],
            }

    result = {
        'root': {
            'target': target,
            'value': service_target_value
        },
        'children': list(response_children_generator())
    }
    return result


def construct_response_for_server_api_view(target: str, parent_json: tuple, children_json: dict,
                                           children_title_order: tuple,
                                           metric_type: str, server: str, service: str = '*', instance: str = '*'):
    server_target_value = parent_json[0]['datapoints'][0][0]

    def response_children_generator():
        for index, value in enumerate(children_json):
            # graphite returns seriesLists in the same order like targets was given
            # so it is possible just to take service_group_title from services_groups_list with the same index
            services_group = children_title_order[index]
            yield {
                'target': construct_target(metric_type, server, services_group, service, instance),
                'value': value['datapoints'][0][0],
            }

    result = {
        'root': {
            'target': target,
            'value': server_target_value
        },
        'children': list(response_children_generator())
    }
    return result


def complex_sg_groups_target_generator(services_group, services: Iterable[str], metric_type: str,
                                       server: str = '*'):
    for service in services:
        target = construct_target(metric_type, server, services_group, service, )
        yield average(summarize(target, "3month", 'avg'))


def complex_services_target_generator(service, instances: Iterable[str], metric_type: str,
                                      server: str = '*', services_group: str = '*'):
    for instance in instances:
        target = construct_target(metric_type, server, services_group, service, instance)
        yield average(summarize(target, "3month", 'avg'))


def complex_server_target_generator(server: str, services_groups: Iterable[str], metric_type: str):
    for services_group in services_groups:
        target = construct_target(metric_type, server, services_group)
        yield average(summarize(str(target), "3month", 'avg'))
