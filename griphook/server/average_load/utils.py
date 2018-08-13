from griphook.server.average_load.strategy.cluster import ClusterStrategy
from griphook.server.average_load.strategy.group import GroupStrategy
from griphook.server.average_load.strategy.server import ServerStrategy
from griphook.server.average_load.strategy.service import ServiceStrategy


def get_strategy_for_target(target_type):
    strategy_class = None
    if target_type == "service":
        strategy_class = ServiceStrategy
    elif target_type == "services_group":
        strategy_class = GroupStrategy
    elif target_type == "server":
        strategy_class = ServerStrategy
    elif target_type == "cluster":
        strategy_class = ClusterStrategy
    return strategy_class
