import click
import datetime
from tabulate import tabulate

from griphook.cli.utils import sql_utils, data_utils

CUSTOM_DATE = data_utils.CustomDateParamType()
session = sql_utils.create_session()


# process == services_group
@click.command()
@click.argument('process', type=click.Choice(data_utils.ServicesChoiceIterator(session)))

@click.option('--mtype',
              type=click.Choice('system_cpu_percent'),
              default='system_cpu_percent',
              help="What type of metrics would you like to get?")
@click.option('--since',  type=CUSTOM_DATE, help="Provide a start date from which to start a query in a form of YEAR-MONTH-YEAR")
@click.option('--until', type=(CUSTOM_DATE, str), help="Provide an end date of a query in a form of YEAR-MONTH-DATE")
# @click.option('--hours',  type=int, default=1, help="For the period of how many hours?")
def grip(process, mtype, since, until):
    """Simple CLI  utillity to print metrics."""
    metrics = sql_utils.make_query(process, mtype, since, until)
    click.echo(tabulate(data_utils.metric_data(metrics), headers="keys", tablefmt="fancy_grid"))


if __name__ == '__main__':
    grip()