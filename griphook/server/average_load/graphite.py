import requests
from griphook.api.graphite.functions import Function, Argument
from griphook.api.graphite.target import Target

average = Function('avg', Argument(Target, name='seriesLists'))

summarize = Function('summarize',
                     Argument(Target, name='seriesList'),
                     Argument(str, name='time', default='1hour', ),
                     Argument(str, name='func', default='sum', ),
                     Argument(bool, name='AlignToFrom', default=False))


def send_graphite_request(params: dict = None) -> str:
    base_url = 'https://graphite.olympus.evo/render'
    response = requests.get(url=base_url, params=params or {}, verify=False)
    return response.text
