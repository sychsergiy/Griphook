import abc
from typing import Optional

import requests


class APIParser(metaclass=abc.ABCMeta):
    """
    API parser inteface. Every API parser should redefine
    fetch() method since the way in order you fetch data from each other API
    differs. This method should implement those details.
    Every parser is synchronous and uses requests.Session
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        self._session = requests.Session()

    @abc.abstractmethod
    def fetch(self,
              time_from: Optional[int] = None,
              time_until: Optional[int] = None) -> str:
        """
        Performs a request and returns plain response data as string
        """
        pass


class GraphiteAPIParser(APIParser):
    """
    Parser with implementation details for Grahite API
    """

    def fetch(self,
              time_from: Optional[int] = None,
              time_until: Optional[int] = None) -> str:

        target = ''\
            'summarize(cantal.*.*.cgroups.*.*.*.{user_cpu_percent,'\
            'system_cpu_percent,vsize},"1hour","max",true)'

        # Parameters for GET request
        params = {
            'format': 'json',
            'target': target
        }

        # Add optional parameters if set
        if time_from is not None:
            params['from'] = time_from
        if time_until is not None:
            params['until'] = time_until

        # Perform GET request via session and return plain data
        return self._session.get(
            self.base_url, params=params, verify=False).text
