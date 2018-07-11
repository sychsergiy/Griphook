from typing import NamedTuple
from json import loads
from re import findall


class Metric(NamedTuple):
    value: float
    type: str
    services_group: str
    service: str


def format_cantal_data(data: str) -> list:
    series_data = loads(data)

    formatted_metrics = []
    for serie in series_data:
        target = (findall(r'\bcantal+.[\w:.-]+', serie['target']))[0].split('.')

        metric = Metric(value=serie['datapoints'][0][0],
                        type=target[7],
                        services_group=target[5].split(':')[0],
                        service=target[5].split(':')[1]
                        )
        formatted_metrics.append(metric)
    return formatted_metrics

