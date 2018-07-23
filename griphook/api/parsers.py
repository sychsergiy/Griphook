from abc import ABCMeta, abstractmethod
from typing import Dict, Tuple, Union

import requests

from griphook.api.exceptions import APIConnectionError

# Type alias for timeout
Timeout = Union[None, float, Tuple[float, float]]


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


class APIParser(GenericParser):
    """
    API parser interface.
    Every parser is synchronous and uses requests.Session
    """

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self._session = requests.Session()

    def request(self,
                method: str = 'GET',
                params: Dict[str, str] = {},
                timeout: Timeout = 20.0) -> str:
        """
        Performs request on base url using session and returns
        text as string.

        :param method: GET, POST, or any that requests module accepts
        :param params: request parameters as dict
        :timeout:
            (float or tuple) – (optional)
            How long to wait for theserver to send data before giving up,
            as a float, or a (connect timeout, read timeout) tuple.
            If set to None - wait until server will respond.
        """
        try:
            response = self._session.request(url=self.base_url,
                                             method=method,
                                             params=params,
                                             timeout=timeout,
                                             verify=False)

            if response.status_code != 200:
                raise APIConnectionError(f'Connection error, '
                                         'status [{response.status_code}]')

            return response.text
        except requests.exceptions.RequestException as e:
            raise APIConnectionError("Connection error") from e
