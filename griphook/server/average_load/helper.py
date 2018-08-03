from griphook.server.average_load.graphite import average, summarize, send_request, construct_target
from griphook.server.models import ServicesGroup, Service
from griphook.server.average_load.abstract import ChartDataHelper


class ServerChartDataHelper(ChartDataHelper):
    def retrieve_children(self) -> tuple:
        services_groups = (
            Service.query
                .filter(Service.server == self.root)
                .join(ServicesGroup).distinct()
                .with_entities(ServicesGroup.title)
        ).all()
        return tuple(services_group_title for (services_group_title,) in services_groups)

    def children_target_constructor(self, children_item) -> str:
        # get average value for each service_group inside this server
        # as service_group can be in few server, calculate only using instances from current server
        # be careful, when you watch average on service_group detail it will be not the same
        return construct_target(self.metric_type, server=self.root, services_group=children_item)

    def root_target_constructor(self) -> str:
        return construct_target(self.metric_type, server=self.root)


class ServicesGroupChartDataHelper(ChartDataHelper):
    # todo: separate query and result normalization
    def retrieve_children(self) -> tuple:
        services = (
            ServicesGroup.query
                .filter(ServicesGroup.title == self.root)
                .join(Service).distinct()
                .with_entities(Service.title)
        ).all()

        # convert to simple structure without nesting
        services = tuple(title for (title,) in services)
        return services

    def children_target_constructor(self, children_item) -> str:
        return construct_target(self.metric_type, services_group=self.root, service=children_item)

    def root_target_constructor(self) -> str:
        return construct_target(self.metric_type, services_group=self.root)


class ServicesChartDataHelper(ChartDataHelper):
    def retrieve_children(self) -> tuple:
        services = (
            Service.query
                .filter(Service.title == self.root).distinct()
                .join(ServicesGroup)
                .with_entities(ServicesGroup.title, Service.title, Service.instance, )
        ).all()
        # necessary to use full path for services
        # because services may have the same name, but relate to different servers
        return services

    def children_target_constructor(self, children_item: tuple) -> str:
        # use format in accordance to `retrieve_children` method returns
        group, service, instance = children_item
        return construct_target(self.metric_type, services_group=group, service=service, instance=instance)

    def root_target_constructor(self) -> str:
        return construct_target(self.metric_type, service=self.root)
