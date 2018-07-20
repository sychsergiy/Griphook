import json
import re
from typing import List, NamedTuple, Optional, Tuple

from pydantic import BaseModel, PydanticValueError, ValidationError, validator

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


class DataSeries(BaseModel):
    target: str
    datapoints: List[Tuple[float, int]]

    @classmethod
    def validate(cls, value):
        if not value['datapoints']:
            return None
        try:
            return super().validate(value)
        except ValidationError:
            return None

    @validator("target")
    def target_validate(cls, value):
        if "cantal" not in value or "lithos" not in value:
            raise WrongTargetStructure(wrong_target=value)
        return value


class CantalData(BaseModel):
    series: List[Optional[DataSeries]]


class WrongTargetStructure(PydanticValueError):
    code = "wrong_target_structure"
    msg_template = "wrong target structure for cantal system, " \
                   "got target:'{wrong_target}'"


def validate_input_cantal_data(decoded_input_data):
    """
    Validates input data according to defined hierarchical data structures.

    :param: decoded data
    :return: valid DataSeries objects
    """
    validated_data = CantalData(series=decoded_input_data)
    # separate None objects from validated data
    filtered_data = filter(lambda x: x, validated_data.series)
    yield from filtered_data


def format_cantal_data(input_data):
    """
    Parses metric target, creates metric object with metric value and with
    information data about service topology.

    :param: row data from Grahite API(cantal metric system)
    :return: metric objects
    """
    try:
        decoded_input_data = json.loads(input_data)
    except json.decoder.JSONDecodeError:
        return

    valid_data = validate_input_cantal_data(decoded_input_data)

    for data_series_object in valid_data:
        # parse metric target according to pattern
        target = CANTAL_PATTERN.match(data_series_object.target)

        metric = Metric(value=round(data_series_object.datapoints[0][0], 5),
                        type=target.group('type'),
                        cluster=target.group('cluster'),
                        server=target.group('server'),
                        services_group=target.group('services_group'),
                        service=target.group('service'),
                        instance=target.group('instance'),
                        )
        yield metric
