import datetime
import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from griphook.api.parsers import GraphiteAPIParser

# To ignore insecure https connection
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def test_fetch_returns_json():
    parser = GraphiteAPIParser("https://graphite.olympus.evo/render")

    time_until = int(datetime.datetime.now().timestamp())
    time_from = int(time_until - datetime.timedelta(hours=1).total_seconds())

    data = parser.fetch(time_from=time_from, time_until=time_until)

    # Check if returns data
    json.loads(data)
