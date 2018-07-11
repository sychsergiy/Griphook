from typing import NamedTuple, Union
from re import findall
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
        target = findall(r'\.([\w:-]+)', serie['target'])

        if serie['datapoints']:
            metric = Metric(value=serie['datapoints'][0][0],
                            type=target[6],
                            services_group=target[4].split(':')[0],
                            service=target[4].split(':')[1]
                            )
            formatted_metrics.append(metric)
    return formatted_metrics
