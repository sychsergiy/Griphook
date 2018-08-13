import json
from typing import Union

import requests
from griphook.api.graphite.functions import Function, Argument
from griphook.api.graphite.target import Target, DotPath

average = Function("avg", Argument(Target, name="seriesLists"))

summarize = Function(
    "summarize",
    Argument(Target, name="seriesList"),
    Argument(str, name="time", default="1hour"),
    Argument(str, name="func", default="sum"),
    Argument(bool, name="AlignToFrom", default=False),
)


def construct_target(
    metric_type, server="*", services_group="*", service="*", instance="*"
):
    path = DotPath(
        "cantal",
        "*",
        f"{server}",
        "cgroups",
        "lithos",
        f"{services_group}:{service}",
        f"{instance}",
    )
    return str(path + metric_type)


class GraphiteAPIError(Exception):
    pass


def send_request(
    target: Union[str, tuple], time_from: int, time_until: int
) -> dict:
    """
    Helper function for sending requests to Graphite APi
    :param target: Graphite API `target` argument,
        str for one target, tuple for multiple
    :param time_from: timestamp
    :param time_until: timestamp
    :return: already parsed to json response
    """
    base_url = "https://graphite.olympus.evo/render"
    params = {
        "format": "json",
        "target": target,
        "from": str(time_from),
        "until": str(time_until),
    }
    # todo: handle connection exception
    response = requests.get(url=base_url, params=params or {}, verify=False)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise GraphiteAPIError("500 status code from Graphite API")
