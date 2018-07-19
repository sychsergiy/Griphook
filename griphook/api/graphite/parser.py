from griphook.api.parsers import APIParser
from griphook.api.graphite.functions import summarize
from griphook.api.graphite.target import Path, MultipleValues


class GraphiteAPIParser(APIParser):
    """
    Parser with implementation details for Graphite API
    """

    def fetch(self, *, time_from: int, time_until: int) -> str:
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
        target = self._construct_target()

        params = {
            'format': 'json',
            'target': target,
            'from': str(time_from),
            'until': str(time_until),
        }

        # Perform GET request via session and return plain data
        return self.request(params=params)

    @staticmethod
    def _construct_target():
        metrics = MultipleValues('user_cpu_percent',
                                 'system_cpu_percent',
                                 'vsize')
        # path to all cpu and memory metrics
        path = Path('cantal', '*', '*', 'cgroups', 'lithos', '*', '*',
                    metrics)

        target = summarize(path, "1hour", "max", True)
        return str(target)
