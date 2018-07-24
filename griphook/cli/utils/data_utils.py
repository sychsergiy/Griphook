from collections import OrderedDict
from datetime import datetime

import click


def metric_data(metrics):
    for metric in metrics:
        yield OrderedDict([
            ('Server', metric.service.server),
            ('Process', metric.service.services_group.title),
            ('Service', metric.service.title),
            ('Instance', metric.service.instance),
            ('Date/Time', metric.time_from),
            ('Metric Type', metric.type.title),
            ('Value', metric.value),
        ])


class CustomDateParamType(click.ParamType):
    name = "CustomDate"

    def convert(self, value, param, ctx):
        try:
            valid_date = datetime.strptime(value, '%Y-%m-%d')
            return valid_date
        except ValueError:
            self.fail('%s is not a valid date' % value, param, ctx)
