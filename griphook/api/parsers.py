from abc import ABCMeta, abstractmethod

import requests

from griphook.api.exceptions import APIConnectionError


class GenericParser(metaclass=ABCMeta):
    """Generic parser interface"""
    @abstractmethod
    def fetch(self, *, time_from: int, time_until: int) -> str:
        """
        Get data with time limits
        Every GenericParser should redefine fetch() method
        This method should implement those details
        """
        pass

    def fetch_one(self, request):
        pass


class APIParser(GenericParser):
    """
    API parser interface.
    Every parser is synchronous and uses requests.Session
    """

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self._session = requests.Session()


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
        try:
            return self._session.get(
                self.base_url, params=params, verify=False).text
        except requests.exceptions.ConnectionError as e:
            raise APIConnectionError(str(e))
