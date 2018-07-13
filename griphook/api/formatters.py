import json
from re import compile
from typing import NamedTuple, Union


class Metric(NamedTuple):
    value: float
    type: str
    services_group: str
    service: str
    instance: str


def format_cantal_data(data: str) -> Union[list, None]:
    """
    Parses metric target, takes data point value and creates metric object
    with parameters.

    :param data: row data from Grahite API(cantal metric system)
    :return: list of metric objects
    """

    try:
        series_data = json.loads(data)
    except json.decoder.JSONDecodeError:
        return None

    formatted_metrics = []
    pattern = compile(".*lithos\."
                      "(?P<services_group>[\w-]+):"
                      "(?P<service>[\w-]+)\."
                      "(?P<instance>[\d])\."
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
                            service=target.group('service'),
                            instance=target.group('instance'),
                            )
            formatted_metrics.append(metric)
    return formatted_metrics


if __name__ == '__main__':
    with open('tests/test_input_data.json', 'r') as data_source:
        test_data = data_source.read()

    res = format_cantal_data(test_data)
    print(res)