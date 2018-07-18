from griphook.api.parsers import APIParser


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

        target = ''\
            'summarize(cantal.*.*.cgroups.lithos.*.*.{user_cpu_percent,'\
            'system_cpu_percent,vsize},"1hour","max",true)'

        # Parameters for GET request
        params = {
            'format': 'json',
            'target': target,
            'from': str(time_from),
            'until': str(time_until),
        }

        # Perform GET request via session and return plain data
        return self.request(params=params)
