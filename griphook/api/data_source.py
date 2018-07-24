from typing import Callable, Dict, List

from griphook.api import parsers


class DataSource:
    def __init__(self, *,
                 parser: parsers.APIParser,
                 data_formatter: Callable[[str], List[Dict]]) -> None:
        """
        DataSource constructor

        :param parser: Object that fetches plain data from source
                       via fetch() method
        :param formatter: Formatter function that will be applied to
                          data that parser returned.
        """
        self.parser = parser
        self.data_formatter = data_formatter

    def read(self, *, time_from: int, time_until: int):
        """
        Reads data from source and returns it

        :param time_from: lower limit of the time interval data will
                          be collected for
        :param time_until: upper limit of time interval
        :returns: formatted data as python objects
        """
        return self.data_formatter(self.parser.fetch(time_from=time_from,
                                                     time_until=time_until))
