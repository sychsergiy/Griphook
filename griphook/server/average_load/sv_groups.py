import json

from griphook.api.graphite.target import MultipleValues, DotPath
from griphook.server.models import ServicesGroup, Service

from griphook.server.average_load.graphite import average, summarize, send_graphite_request
from griphook.server.average_load.helper import construct_response_for_services_groups_api_view, \
    complex_target_generator


def get_average_services_group_load_chart_data(services_group: str, time_from: int, time_until: int,
                                               metric_type: str):
    services = (
        ServicesGroup.query
            .filter(ServicesGroup.title == services_group)
            .join(Service).distinct()
            .with_entities(Service.title)
    ).all()

    # convert to simple structure
    services = tuple(title for (title,) in services)

    # create service_groups part of graphite target: '({service_group_title1:*, service_group_title2:*, ...})'
    target_instances = MultipleValues(*[f'{services_group}:{services}' for services in services])
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
    complex_target = list(complex_target_generator('services_group', metric_type, services_group, services, ))
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

    target = f'cantal.*.*.cgroups.lithos.{services_group}:*'
    response_data = construct_response_for_services_groups_api_view(
        target, sv_group_average_response_json, services_average_response_json,
        services, metric_type, services_group=services_group)
    return response_data
