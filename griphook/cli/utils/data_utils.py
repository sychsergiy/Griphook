import click
from datetime import datetime
from collections import OrderedDict

from griphook.cli.utils.sql_utils import all_groups


def metric_data(metrics):
    for metric in metrics:
        yield OrderedDict([
            ('Server', metric.service.server),
            ('Process', metric.service.services_group.title),
            ('Service', metric.service.title),
            ('Instance', metric.service.instance),
            ('Date/Time', metric.batch.time),
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


class ServicesChoiceIterator(object):
    def __init__(self, session):
        self.services = []
        groups = all_groups(session)
        for group in groups:
            self.services.append(group.title)

    def __iter__(self):
        # Get list of services and assign it to self.services
        return iter(self.services)
