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
    pattern = compile(".*lithos\."
                      "(?P<services_group>[\w-]+):"
                      "(?P<service>[\w-]+)\..*\."
                      "(?P<type>[\w-]+)"
                      )
    for serie in series_data:
        target = pattern.match(serie['target'])

        try:
            datapoint_value = serie['datapoints'][0][0]
        except IndexError:
            continue

        if datapoint_value is not None:
            metric = Metric(value=round(datapoint_value, 5),
                            type=target.group('type'),
                            services_group=target.group('services_group'),
                            service=target.group('service')
                            )
            formatted_metrics.append(metric)
    return formatted_metrics
