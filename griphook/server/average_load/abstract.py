from griphook.server.average_load.graphite import average, summarize, send_request


# todo: better name for this class
class ChartDataHelper(object):
    """
    Helper class for average services load endpoints.
    Provide convenient interface to work with services
     hierarchy(cluster, server, service_group, service, instance)
    Flexible interface for constructing `target` argument for each item in hierarchy
    """

    def __init__(self, root: str, metric_type: str):
        self.root: str = root
        self.metric_type: str = metric_type
        self.children: tuple = self.retrieve_children()

    def retrieve_children(self) -> tuple:
        """
        Retrieve children instances for root:
         servers for cluster
         services groups for server
         services for services group

        Basically this method makes db query and returns tuple of children_items,
        format of children_item format is arbitrary, but keep in mind that
        `children_target_constructor` method retrieves it as argument

        :return: tuple[any], mostly tuple[str], tuple[tuple[str]] for services
        """
        # todo graphite avg function can't receive empty list
        raise NotImplementedError

    def children_target_constructor(self, children_item) -> str:
        """
        Each inherited item in hierarchy(cluster, server, service_group, service)
         has it own logic of constructing `target` argument for Graphite api, implement it here.
        :param children_item: item from collection returned by `retrieve_children` method, keep in mind!
        :return: path to objects to be obtained from API
        """
        raise NotImplementedError

    def root_target_constructor(self) -> str:
        """
        Each inherited item in hierarchy(cluster, server, service_group, service)
         has it own logic of constructing `target` argument for Graphite api, implement it here.
        :return:
        """
        raise NotImplementedError

    def root_target(self):
        target = self.root_target_constructor()
        return average(summarize(target, "3month", "avg"))

    def children_target(self) -> str:
        """
        Generator for creating complex(multiple) `target` argument for Graphite API
         converted into Graphite average and summarize functions
        :return: constructed target for one children_item:
            avg(summarize(cantal.*.*.cgroups.lithos.adv-stable:adv-ua.*.vsize,"3month","avg",false))
        """
        for item in self.children:
            target = self.children_target_constructor(item)
            yield average(summarize(target, "3month", 'avg'))

    def get_data(self, time_from: int, time_until: int) -> dict:
        """
        Function sending request to Graphite API and
         converting response to convenient format
        :param time_from: timestamp
        :param time_until: timestamp
        :return:
        """
        # target to root
        root_target = self.root_target()
        # target without wraps of avg and summarize functions
        # more user friendly format for showing on hover in chart
        root_target_to_visualize = self.root_target_constructor()

        # send request to Graphite API with root target
        parent_response = send_request(root_target, time_from, time_until)

        # parse json
        root_response_value = parent_response[0]['datapoints'][0][0]

        root_data = {'target': root_target_to_visualize, 'value': root_response_value}

        # tuple of targets(item is target for each children_item) for sending multiple target argument
        children_target = tuple(self.children_target())
        # send request to Graphite API with root target
        children_response = send_request(children_target, time_from, time_until)
        # convert response to convenient form
        children_data = [{
            'target': self.children_target_constructor(self.children[index]),
            'value': value['datapoints'][0][0],  # todo: check IndexError
        } for index, value in enumerate(children_response)]

        result = {
            'root': root_data,
            'children': children_data
        }
        # todo: refactor this method
        return result
