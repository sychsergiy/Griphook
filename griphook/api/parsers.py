import abc

import requests

from griphook.api.exceptions import APIConnectionError


class APIParser(metaclass=abc.ABCMeta):
    """
    API parser interface. Every API parser should redefine
    fetch() method since the way in order you fetch data from each other API
    differs. This method should implement those details.
    Every parser is synchronous and uses requests.Session
    """

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self._session = requests.Session()

    @abc.abstractmethod
    def fetch(self, *, time_from: int, time_until: int) -> str:
        """
        Performs a request and returns plain response data as string
        """
        pass


class GraphiteAPIParser(APIParser):
    """
    Parser with implementation details for Graphite API
    """

    def fetch(self, *, time_from: int, time_until: int) -> str:

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
        try:
            return self._session.get(
                self.base_url, params=params, verify=False).text
        except requests.exceptions.ConnectionError as e:
            raise APIConnectionError(str(e))
