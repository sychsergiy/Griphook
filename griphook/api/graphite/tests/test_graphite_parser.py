from urllib.parse import parse_qsl, urlparse

import pytest
from httmock import HTTMock, urlmatch

from griphook.api.graphite.parser import GraphiteAPIParser


@pytest.fixture(scope="session")
def url():
    return "http://example.com/example"


@pytest.fixture
def parser(url):
    return GraphiteAPIParser(url)


def test_request(parser):
    target = "my.custom.target"
    time_from, time_until = "123", "456"

    desired_params = {
        "target": target,
        "from": time_from,
        "until": time_until,
        "format": "json",
    }

    netloc = urlparse(parser.base_url).netloc

    # Main test function that intercepts requests and validates them
    @urlmatch(netloc=netloc)
    def fetch_mock(url, request):
        # If number of params and desired matches and all
        # of desired are in request.params, then test is passed

        actual_params = dict(parse_qsl(urlparse(request.url).query))
        assert len(desired_params) == len(actual_params)
        for key in desired_params:
            assert actual_params[key] == desired_params[key]

        return "All good"

    # Run the test
    with HTTMock(fetch_mock):
        parser.fetch(time_from=time_from, time_until=time_until, target=target)
