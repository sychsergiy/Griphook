import datetime
import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from griphook.api.data_source import DataSource
from griphook.api.parsers import GraphiteAPIParser
from griphook.api.formatters import format_cantal_data


# To ignore insecure https connection
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

TIME_UNTIL = int(datetime.datetime.now().timestamp())
TIME_FROM = int(TIME_UNTIL - datetime.timedelta(hours=1).total_seconds())
PARSER = GraphiteAPIParser("https://graphite.olympus.evo/render")


def test_parser_fetch_returns_json():
    data = PARSER.fetch(time_from=TIME_FROM, time_until=TIME_UNTIL)
    # If returns valid data - no exception will be raised, so test is passed
    json.loads(data)


def test_data_source_read():
    ds = DataSource(parser=PARSER, data_formatter=format_cantal_data)
    ds.read(time_from=TIME_FROM, time_until=TIME_UNTIL)
