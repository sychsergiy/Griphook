import json
from typing import Iterable, Tuple

from griphook.api.graphite.target import MultipleValues, DotPath
from griphook.server.models import ServicesGroup, Service

from griphook.server.average_load.graphite import average, summarize, send_graphite_request


def get_average_services_group_load_chart_data(service_group: str, time_from: int, time_until: int,
                                               metric_type: str):
    services = (
        ServicesGroup.query
            .filter(ServicesGroup.title == service_group)
            .join(Service).distinct()
            .with_entities(Service.title)
    ).all()

    # convert to simple structure
    services_titles = tuple(title for (title,) in services)

    # create service_groups part of graphite target: '({service_group_title1:*, service_group_title2:*, ...})'
    target_instances = MultipleValues(*[f'{service_group}:{sv_title}' for sv_title in services_titles])
    # todo: do I really need to insert services here or just take all from services_groups

    # create_path
    path_to_instances = DotPath('cantal', '*', '*', 'cgroups', 'lithos', f'{target_instances}', '*')
    path_with_metric = str(path_to_instances + metric_type)
    # todo: add filter by server if given

    full_target = average(summarize(path_with_metric, "3month", 'avg'))
    params = {
        'format': 'json',
        'target': full_target,
        'from': str(time_from),
        'until': str(time_until),
    }
    sv_group_average_response = send_graphite_request(params)  # get average value for server

    # construct query with multiple targets -------------------------------------------
    complex_target = list(complex_target_generator(service_group, services_titles, metric_type))
    params = {
        'format': 'json',
        'target': complex_target,
        'from': str(time_from),
        'until': str(time_until),
    }
    services_average_response = send_graphite_request(params=params)

    # ------------------------------------------------------------------------------------------
    sv_group_average_response_json = json.loads(sv_group_average_response)
    services_average_response_json = json.loads(services_average_response)

    response_data = construct_response_for_server_api_view(sv_group_average_response_json,
                                                           services_average_response_json,
                                                           service_group, services_titles, metric_type)

    return response_data


def complex_target_generator(service_group, services_titles: Iterable[str], metric_type: str, server: str = None):
    server_part = server or '*'
    for service_title in services_titles:
        path_to_instances = DotPath('cantal', '*', f'{server_part}', 'cgroups', 'lithos',
                                    f'{service_group}:{service_title}', '*')
        path_with_metric = str(path_to_instances + metric_type)
        yield average(summarize(path_with_metric, "3month", 'avg'))


def construct_response_for_server_api_view(parent_json: tuple, children_json: dict, service_group: str,
                                           children_title_order: Tuple[str],
                                           metric_type: str, server: str = '*'):
    # todo: use target prefix
    service_group_target = f'cantal.*.{server}.cgroups.lithos.{service_group}:*'
    service_group_target_value = parent_json[0]['datapoints'][0][0]

    def response_children_generator():
        for index, value in enumerate(children_json):
            # graphite returns seriesLists in the same order like targets was given
            # so it is possible just to take service_group_title from services_groups_list with the same index
            service_title = children_title_order[index]
            # todo: target must be constructed with parameters, depends on view(server, sv_group, service)
            path = DotPath('cantal', '*', f'{server}', 'cgroups', 'lithos', f'{service_group}:{service_title}', '*')
            target = str(path + metric_type)
            yield {
                'target': target,
                'value': value['datapoints'][0][0],
            }

    result = {
        'root': {
            'target': service_group_target,
            'value': service_group_target_value
        },
        'children': list(response_children_generator())
    }
    return result
