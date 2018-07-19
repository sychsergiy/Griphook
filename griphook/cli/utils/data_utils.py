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


class ServicesChoiceIterator(object):
    def __init__(self, session):
        self.session = session
        self.services = []

    def __iter__(self):
        # Get list of services and assign it to self.services
        #  fill it
        for group in all_groups(self.session):
            print(type(group))
            self.services.append(group)

        return iter(self.services)

