import json

from typing import Iterable

from griphook.api.graphite.target import MultipleValues, DotPath

from griphook.server.average_load.graphite import average, summarize, send_graphite_request
from griphook.server.models import Service, ServicesGroup


def get_server_load_chart_data(server: str, time_from: int, time_until: int, metric_type: str):
    # todo avg function can't receive empty list`

    # get server service_groups in format  [(service_group_title1, ), (service_group_title2, ) ...]
    services_groups = (
        Service.query
            .filter(Service.server == server)
            .join(ServicesGroup).distinct()
            .with_entities(ServicesGroup.title)
    ).all()
    # convert to simple tuple with titles
    services_groups_titles = tuple(services_group_title for (services_group_title,) in services_groups)

    # create service_groups part of graphite target: '({service_group_title1:*, service_group_title2:*, ...})'
    target_instances = MultipleValues(*[f'{sv_title}:*' for sv_title in services_groups_titles])
    # todo: do I really need to insert service_groups here or just take all from server

    # create_path
    path_to_instances = DotPath('cantal', '*', f'{server}', 'cgroups', 'lithos', f'{target_instances}', '*')
    path_with_metric = str(path_to_instances + metric_type)

    full_target = average(summarize(path_with_metric, "3month", 'avg'))
    params = {
        'format': 'json',
        'target': full_target,
        'from': str(time_from),
        'until': str(time_until),
    }
    server_average_response = send_graphite_request(params)  # get average value for server

    # construct query with multiple targets
    complex_target = list(complex_target_generator(server, services_groups_titles, metric_type))

    params = {
        'format': 'json',
        'target': complex_target,
        'from': str(time_from),
        'until': str(time_until),
    }

    # get average value for each service_group
    # as service_group can be in few server, calculate only using instances from current server
    # be careful, when you watch average for service_group it will be not the same
    service_group_average = send_graphite_request(params=params)

    server_average_response_json = json.loads(server_average_response)
    service_group_average_json = json.loads(service_group_average)

    response_data = construct_response_for_server_api_view(server_average_response_json, service_group_average_json,
                                                           server, services_groups_titles, metric_type)
    return response_data


def complex_target_generator(server: str, services_groups_titles: Iterable[str], metric_type: str):
    for sv_title in services_groups_titles:
        path = DotPath('cantal', '*', f'{server}', 'cgroups', 'lithos', f'{sv_title}:*', '*')
        yield average(summarize(str(path + metric_type), "3month", 'avg'))


def construct_response_for_server_api_view(parent_json: tuple, children_json: dict, server: str,
                                           children_title_order: tuple,
                                           metric_type: str):
    # todo: use target prefix
    server_target = f'cantal.*.{server}.cgroups.lithos.*'
    server_target_value = parent_json[0]['datapoints'][0][0]

    def response_children_generator():
        for index, value in enumerate(children_json):
            # graphite returns seriesLists in the same order like targets was given
            # so it is possible just to take service_group_title from services_groups_list with the same index
            service_group_title = children_title_order[index]
            # todo: target must be constructed with parameters, depends on view(server, sv_group, service)
            path = DotPath('cantal', '*', f'{server}', 'cgroups', 'lithos', f'{service_group_title}:*', '*')
            target = str(path + metric_type)
            yield {
                'target': target,
                'value': value['datapoints'][0][0],
            }

    result = {
        'root': {
            'target': server_target,
            'value': server_target_value
        },
        'children': list(response_children_generator())
    }
    return result
