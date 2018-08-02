import json
import requests

from typing import Union

from griphook.api.graphite.target import DotPath
from griphook.server.average_load.graphite import average, summarize
from griphook.server.models import ServicesGroup, Service


def construct_target(metric_type, server='*', services_group='*', service='*', instance='*'):
    path = DotPath('cantal', '*', f'{server}', 'cgroups', 'lithos', f'{services_group}:{service}', f'{instance}')
    return str(path + metric_type)


class ChartDataHelper(object):
    def __init__(self, parent: str, metric_type: str):
        self.parent: str = parent
        self.children: tuple = self.retrieve_children()
        self.metric_type: str = metric_type

    def retrieve_children(self):
        # todo graphite-avg function can't receive empty list
        raise NotImplementedError

    def children_target_constructor(self, children_item):
        raise NotImplementedError

    def root_target_constructor(self):
        raise NotImplementedError

    def root_target(self):
        target = self.root_target_constructor()
        return average(summarize(target, "3month", "avg"))

    def children_target(self):
        # construct query with multiple targets
        for item in self.children:
            target = self.children_target_constructor(item)
            yield average(summarize(target, "3month", 'avg'))

    def get_data(self, time_from, time_until):
        root_target = self.root_target()
        children_target = tuple(self.children_target())

        parent_response = send_request(root_target, time_from, time_until)
        children_response = send_request(children_target, time_from, time_until)

        # parse json
        root_response_value = parent_response[0]['datapoints'][0][0]
        children_response_value = [{
            'target': self.children_target_constructor(self.children[index]),
            'values': value['datapoints'][0][0],
        } for index, value in enumerate(children_response)]

        root_target_to_visualize = self.root_target_constructor()

        response = {
            'root': {'target': root_target_to_visualize, 'value': root_response_value},
            'children': children_response_value
        }
        return response


def services_group_target_getter(metric_type, parent, children_item):
    construct_target(metric_type, server=parent, services_group=children_item)


class ServerChartDataHelper(ChartDataHelper):
    def __init__(self, *args, **kwargs):
        super(ServerChartDataHelper, self).__init__(*args, **kwargs)

    def retrieve_children(self) -> tuple:
        services_groups = (
            Service.query
                .filter(Service.server == self.parent)
                .join(ServicesGroup).distinct()
                .with_entities(ServicesGroup.title)
        ).all()
        return tuple(services_group_title for (services_group_title,) in services_groups)

    def children_target_constructor(self, children_item) -> str:
        # get average value for each service_group inside this server
        # as service_group can be in few server, calculate only using instances from current server
        # be careful, when you watch average on service_group detail it will be not the same
        return construct_target(self.metric_type, server=self.parent, services_group=children_item)

    def root_target_constructor(self) -> str:
        return construct_target(self.metric_type, server=self.parent)


class ServicesGroupChartDataHelper(ChartDataHelper):
    def retrieve_children(self) -> tuple:
        services = (
            ServicesGroup.query
                .filter(ServicesGroup.title == self.parent)
                .join(Service).distinct()
                .with_entities(Service.title)
        ).all()

        # convert to simple structure
        services = tuple(title for (title,) in services)
        return services

    def children_target_constructor(self, children_item) -> str:
        return construct_target(self.metric_type, services_group=self.parent, service=children_item)

    def root_target_constructor(self) -> str:
        return construct_target(self.metric_type, services_group=self.parent)


class ServicesChartDataHelper(ChartDataHelper):
    def retrieve_children(self) -> tuple:
        services = (
            Service.query
                .filter(Service.title == self.parent).distinct()
                .join(ServicesGroup)
                .with_entities(Service.server, ServicesGroup.title, Service.title, Service.instance, )
        ).all()
        return services

    def children_target_constructor(self, children_item) -> str:
        server, group, service, instance = children_item
        return construct_target(self.metric_type, server=server, services_group=group, service=service,
                                instance=instance)

    def root_target_constructor(self) -> str:
        return construct_target(self.metric_type, service=self.parent)


def send_request(target: Union[str, tuple], time_from: int, time_until: int) -> dict:
    base_url = 'https://graphite.olympus.evo/render'
    params = {
        'format': 'json',
        'target': target,
        'from': str(time_from),
        'until': str(time_until),
    }
    # todo: handle connection exception
    response = requests.get(url=base_url, params=params or {}, verify=False)
    return json.loads(response.text)
