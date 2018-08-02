import json
import requests

from griphook.api.graphite.target import DotPath
from griphook.server.average_load.graphite import average, summarize
from griphook.server.models import ServicesGroup, Service


def construct_target(metric_type, server='*', services_group='*', service='*', instance='*'):
    path = DotPath('cantal', '*', f'{server}', 'cgroups', 'lithos', f'{services_group}:{service}', f'{instance}')
    return str(path + metric_type)


class ChartDataHelper(object):
    def __init__(self, parent: str, metric_type: str):
        self.parent: str = parent
        self.children: tuple = self.get_children()
        self.metric_type: str = metric_type

    def get_children(self):
        # todo graphite-avg function can't receive empty list
        raise NotImplementedError

    def children_target_getter(self, children_item):
        raise NotImplementedError

    def parent_target_getter(self):
        raise NotImplementedError

    def parent_target(self):
        target = self.parent_target_getter()
        return average(summarize(target, "3month", "avg"))

    def children_target(self):
        # construct query with multiple targets
        for item in self.children:
            target = self.children_target_getter(item)
            yield average(summarize(target, "3month", 'avg'))

    def get_data(self, time_from, time_until):
        parent_target = self.parent_target()

        children_target = tuple(self.children_target())

        helper = GraphiteHelper(parent_target, children_target, time_from, time_until)

        parent_response = helper.send_request()
        children_response = helper.send_request(for_children=True)

        # parse json
        parent_response_value = parent_response[0]['datapoints'][0][0]

        def response_children_generator():
            for index, value in enumerate(children_response):
                # graphite returns seriesLists in the same order like targets was given
                # so it is possible just to take service_group_title from services_groups_list with the same index
                children_item = self.children[index]
                yield {
                    'target': self.children_target_getter(children_item),
                    'value': value['datapoints'][0][0],
                }

        children_response_value = list(response_children_generator())

        parent_target_to_visualize = self.parent_target_getter()
        result = helper.construct_response(parent_target_to_visualize, parent_response_value, children_response_value)
        return result


def services_group_target_getter(metric_type, parent, children_item):
    construct_target(metric_type, server=parent, services_group=children_item)


class ServerChartDataHelper(ChartDataHelper):
    def get_children(self) -> tuple:
        services_groups = (
            Service.query
                .filter(Service.server == self.parent)
                .join(ServicesGroup).distinct()
                .with_entities(ServicesGroup.title)
        ).all()
        # convert to simple tuple with titles
        return tuple(services_group_title for (services_group_title,) in services_groups)

    def children_target_getter(self, children_item) -> str:
        # get average value for each service_group inside this server
        # as service_group can be in few server, calculate only using instances from current server
        # be careful, when you watch average for service_group it will be not the same
        return construct_target(self.metric_type, server=self.parent, services_group=children_item)

    def parent_target_getter(self) -> str:
        return construct_target(self.metric_type, server=self.parent)


class ServicesGroupChartDataHelper(ChartDataHelper):
    def get_children(self) -> tuple:
        services = (
            ServicesGroup.query
                .filter(ServicesGroup.title == self.parent)
                .join(Service).distinct()
                .with_entities(Service.title)
        ).all()

        # convert to simple structure
        services = tuple(title for (title,) in services)
        return services

    def children_target_getter(self, children_item) -> str:
        return construct_target(self.metric_type, services_group=self.parent, service=children_item)

    def parent_target_getter(self) -> str:
        return construct_target(self.metric_type, services_group=self.parent)


class ServicesChartDataHelper(ChartDataHelper):
    def get_children(self) -> tuple:
        services = (
            Service.query
                .filter(Service.title == self.parent).distinct()
                .with_entities(Service.instance)
        ).all()
        return tuple(instance for (instance,) in services)

    def children_target_getter(self, children_item) -> str:
        # todo: this part is wrong, services group can't be all,
        # todo: services in different services groups are different services
        return construct_target(self.metric_type, service=self.parent, instance=children_item)

    def parent_target_getter(self) -> str:
        return construct_target(self.metric_type, service=self.parent)


class GraphiteHelper(object):
    def __init__(self, parent_target: str, children_target: tuple, time_from: int, time_until: int):
        self.parent_target: tuple = parent_target
        self.children_target = children_target

        self.time_from = time_from
        self.time_until = time_until

    def send_request(self, for_children: bool = False) -> dict:
        base_url = 'https://graphite.olympus.evo/render'
        target = self.children_target if for_children else self.parent_target
        params = {
            'format': 'json',
            'target': target,
            'from': str(self.time_from),
            'until': str(self.time_until),
        }
        # todo: handle connection exception
        response = requests.get(url=base_url, params=params or {}, verify=False)
        return json.loads(response.text)

    @staticmethod
    def construct_response(target_to_visualize: str, parent_value: int, children_values: list) -> dict:
        root_part = {
            'target': target_to_visualize,
            'value': parent_value
        }
        result = {
            'root': root_part,
            'children': children_values
        }
        return result
