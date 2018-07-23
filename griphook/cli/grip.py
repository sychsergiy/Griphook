from typing import List

import click
from tabulate import tabulate

from griphook.cli.utils import sql_utils, data_utils

CUSTOM_DATE = data_utils.CustomDateParamType()
SESSION = sql_utils.create_session()
METRIC_TYPE_OPTIONS: List[str] = ['system_cpu_percent', 'user_cpu_percent', 'vsize']
SERVICES_GROUPS = data_utils.ServicesChoiceIterator(SESSION)


@click.command()
@click.argument('process', type=click.Choice(SERVICES_GROUPS))
@click.option('--mtype',
              type=click.Choice(METRIC_TYPE_OPTIONS),
              default='system_cpu_percent',
              help="What type of metrics would you like to get?")
@click.option('--since',  type=CUSTOM_DATE, help="Provide a start date from which to start a query in a form of YEAR-MONTH-YEAR")
@click.option('--until', type=CUSTOM_DATE, help="Provide an end date of a query in a form of YEAR-MONTH-DATE")
def grip(process, mtype, since, until, group): # Don't forget to rename this
    """Simple CLI  utility to show metrics."""

    metrics = sql_utils.make_query(SESSION, process, mtype, since, until, group)
    click.echo(tabulate(data_utils.metric_data(metrics), headers="keys", tablefmt="fancy_grid"))


if __name__ == '__main__':
    grip()