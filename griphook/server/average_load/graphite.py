import requests
import json

from typing import Iterable
from griphook.api.graphite.functions import Function, Argument
from griphook.api.graphite.target import MultipleValues, Target, DotPath

from griphook.server.models import Service, ServicesGroup

# Built-in functions
average = Function('avg', Argument(Target, name='seriesLists'))

summarize = Function('summarize',
                     Argument(Target, name='seriesList'),
                     Argument(str, name='time', default='1hour', ),
                     Argument(str, name='func', default='sum', ),
                     Argument(bool, name='AlignToFrom', default=False))


def get_server_load_chart_data(server: str, time_from: int, time_until: int, metric_type: str):
    # todo avg function can't receive empty list`

    # get server service_groups in format  [(service_group_title1, ), (service_group_title2, ) ...]
    server_services_groups = (
        Service.query
            .filter(Service.server == server)
            .join(ServicesGroup).distinct()
            .with_entities(ServicesGroup.title, )
    ).all()

    # create service_groups part of graphite target: '({service_group_title1:*, service_group_title2:*, ...})'
    target_services = MultipleValues(*[f'{service_group_title}:*' for (service_group_title,) in server_services_groups])

    path = DotPath('cantal', '*', f'{server}', 'cgroups', 'lithos', f'{target_services}', '*')

    target = average(summarize(str(path + metric_type), "3month", 'avg'))
    params = {
        'format': 'json',
        'target': target,
        'from': str(time_from),
        'until': str(time_until),
    }
    server_average_response = send_graphite_request(params)  # get average value for server
    # print(server_average_response)

    complex_target = list(complex_target_generator(server, server_services_groups, metric_type))
    # construct query with multiple targets
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

    server_target = f'cantal.*.{server}'
    server_target_value = json.loads(server_average_response)[0]['datapoints'][0][0]

    service_group_average_json = json.loads(service_group_average)

    def response_children_generator():
        for index, value in enumerate(service_group_average_json):
            # graphite returns seriesLists in the same order like targets was given
            # so it is possible just to take service_group_title from services_groups_list with the same index
            service_group_title = server_services_groups[index][0]
            yield {
                'target': f'cantal.*.{server}.cgroups.lithos.{service_group_title}:*.*.{metric_type}',
                'value': value['datapoints'][0][0],
            }

    response_data = {
        'parent': {
            'target': server_target,
            'value': server_target_value
        },
        'children': list(response_children_generator())
    }
    return response_data


def complex_target_generator(server: str, server_services_groups: Iterable[str], metric_type: str):
    for (service_group_title,) in server_services_groups:
        path = DotPath('cantal', '*', f'{server}', 'cgroups', 'lithos', f'{service_group_title}:*', '*')
        yield average(summarize(str(path + metric_type), "3month", 'avg'))


def send_graphite_request(params: dict = None) -> str:
    """
    Performs request on base url using session and returns
    text as string.

    :param method: GET, POST, or any that requests module accepts
    :param params: request parameters as dict
    :timeout:
        (float or tuple) – (optional)
        How long to wait for theserver to send data before giving up,
        as a float, or a (connect timeout, read timeout) tuple.
        If set to None - wait until server will respond.
    """

    base_url = 'https://graphite.olympus.evo/render'
    response = requests.get(url=base_url, params=params or {}, verify=False)

    return response.text


def get_average_services_group_load_chart_data(service_group: str, services: list, time_from: int,
                                               time_until: int):
    # response = send_graphite_request(time_from, time_until, metric_type) # use response from stub

    # converted_multipe_values = MultipleValues(*services)
    return mock_api_response()


def get_average_service_load_chart_data(service: str, services: list, time_from: int, time_until: int):
    # converted_multipe_values = MultipleValues(*services)
    # response = send_graphite_request(time_from, time_until, metric_type) # use response from stub
    return mock_api_response()


def mock_api_response():
    from griphook.server.average_load.mock import result
    return result
