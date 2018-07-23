import click
from datetime import datetime

from griphook.cli.utils.sql_utils import all_groups


def metric_data(metrics):
    for metric in metrics:
        yield {
            'Server': metric.service.server,
            'Process': metric.service.services_group.title,
            'Service': metric.service.title,
            'Instance': metric.service.instance,
            'Date/Time': metric.batch.time,
            'Metric Type': metric.type.title,
            'Value': metric.value
        }

        # yield OrderedDict([
        #     ('Server', metric.service.server),
        #     ('Process', metric.service.services_group.title),
        #     ('Service', metric.service.title),
        #     ('Instance', metric.service.instance),
        #     ('Date/Time', metric.batch.time),
        #     ('Metric Type', metric.type.title),
        #     ('Value', metric.value),
        # ])


class CustomDateParamType(click.ParamType):
    name = "CustomDate"

    def convert(self, value, param, ctx):
        try:
            return datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            self.fail('%s is not a valid date' % value, param, ctx)


class ServicesChoiceIterator(object):
    def __init__(self, session):
        self.services = [g.title for g in all_groups(session)]

    def __iter__(self):
        # Get list of services and assign it to self.services
        return iter(self.services)
