import json
import re
from typing import *

from pydantic import BaseModel, ValidationError, validator


CANTAL_PATTERN = re.compile(".*\."
                            "(?P<cluster>[\w]+)\."
                            "(?P<server>[\w]+)\.cgroups\.lithos\."
                            "(?P<services_group>[\w-]+):"
                            "(?P<service>[\w-]+)\."
                            "(?P<instance>[\w-]+)\."
                            "(?P<type>[\w-]+)")


class Metric(NamedTuple):
    value: float
    type: str
    cluster: str
    server: str
    services_group: str
    service: str
    instance: str


class DataSeries(BaseModel): #TODO: change datatypes, add check empty list
    target: str
    datapoints: List[List[Union[float, int]]]

    @classmethod
    def validate(cls, value):
        try:
            return super().validate(value)
        except ValidationError:
            return None

    @validator('target')
    def target_must_contain_cantal(cls, value):
        if ('cantal' and 'lithos') not in value:
            raise ValidationError
        return value


class Data(BaseModel):
    series: List[Optional[DataSeries]]


def filter_input_data(data_series):
    valid_data = Data(series=data_series)
    yield from filter(lambda x: x, valid_data.series)


def format_cantal_data(input_data):
    """
    Parses metric target, takes data point value and creates metric object
    with parameters.

    :param input_data: row data from Grahite API(cantal metric system)
    :return: metric objects
    """
    try:
        series_data = json.loads(input_data)
    except json.decoder.JSONDecodeError:
        return

    filtered_series_list = filter_input_data(series_data)

    for data in filtered_series_list:
        target = CANTAL_PATTERN.match(data.target)

        metric = Metric(value=round(data.datapoints[0][0], 5),
                        type=target.group('type'),
                        cluster=target.group('cluster'),
                        server=target.group('server'),
                        services_group=target.group('services_group'),
                        service=target.group('service'),
                        instance=target.group('instance'),
                        )
        yield metric
