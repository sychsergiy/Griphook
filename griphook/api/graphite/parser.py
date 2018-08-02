from typing import Optional

from griphook.api.graphite.functions import summarize
from griphook.api.graphite.target import DotPath, MultipleValues
from griphook.api.parsers import APIParser


class GraphiteAPIParser(APIParser):
    """
    Parser with implementation details for Graphite API
    """
    __path = DotPath('cantal', '*', '*', 'cgroups', 'lithos', '*', '*')
    __metrics = MultipleValues('user_cpu_percent',
                               'system_cpu_percent',
                               'vsize')

    def fetch(self, *,
              time_from: int,
              time_until: int,
              target: Optional[str] = None) -> str:
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
        target = target or self.__construct_default_target()

        params = {
            'format': 'json',
            'target': target,
            'from': str(time_from),
            'until': str(time_until),
        }
        print(params)
        # Perform GET request via session and return plain data
        return self.request(params=params)

    def __construct_default_target(self) -> str:

        # path to all cpu and memory metrics
        path = self.__path + str(self.__metrics)

        target = summarize(path, "1hour", "max", True)
        return str(target)
