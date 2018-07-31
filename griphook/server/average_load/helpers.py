from api.graphite.target import DotPath


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

    return {
        'parent': {
            'target': server_target,
            'value': server_target_value
        },
        'children': list(response_children_generator())
    }
