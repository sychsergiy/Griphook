from typing import Optional, Union

from griphook.api.graphite.functions import (
    summarize,
    Function,
    BuiltInOrTarget,
    Argument,
)
from griphook.api.graphite.target import DotPath, MultipleValues
from griphook.api.parsers import APIParser


class GraphiteAPIParser(APIParser):
    """
    Parser with implementation details for Graphite API
    """

    __path = DotPath("cantal", "*", "*", "cgroups", "lithos", "*", "*")
    __metrics = MultipleValues(
        "user_cpu_percent", "system_cpu_percent", "vsize"
    )
    __default_function = summarize

    def fetch(
        self, *, time_from: int, time_until: int, target: Optional[str] = None
    ) -> str:
        """
        Fetch all metric data for CPU and RAM from Graphite API

        :param time_from: timestamp for lower time limit
        :type time_from: int
        :param time_until: timestamp for upper time limit
        :type time_until: int
        :returns: json-formatted string
        :raises: APIConnectionError
        """

        # Parameters for GET request
        target = target or GraphiteAPIParser.construct_target()

        params = {
            "format": "json",
            "target": target,
            "from": str(time_from),
            "until": str(time_until),
        }
        # Perform GET request via session and return plain data
        return self.request(params=params)

    @classmethod
    def construct_target(
        cls,
        path: Optional[DotPath] = None,
        metrics: Optional[str] = None,
        function: Optional[Function] = None,
        *func_args: Union[BuiltInOrTarget, Argument]
    ) -> str:
        path = path or cls.__path
        metrics = metrics or str(cls.__metrics)
        function = function or cls.__default_function
        args = func_args or ("1hour", "max", True)

        target = function(path + metrics, *args)
        return str(target)
