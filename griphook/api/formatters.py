from typing import NamedTuple, Union
from re import compile
import json


class Metric(NamedTuple):
    value: float
    type: str
    services_group: str
    service: str


def format_cantal_data(data: str) -> Union[list, None]:
    try:
        series_data = json.loads(data)
    except json.decoder.JSONDecodeError:
        return None

    formatted_metrics = []
    for serie in series_data:
        pattern = compile('\.([\w:-]+)')
        target = pattern.findall(serie['target'])

        if serie['datapoints'] and serie['datapoints'][0][0] is not None:
            try:
                metric = Metric(value=round(serie['datapoints'][0][0], 5),
                                type=target[6],
                                services_group=target[4].split(':')[0],
                                service=target[4].split(':')[1]
                                )
            except IndexError:
                continue

            formatted_metrics.append(metric)
    return formatted_metrics
