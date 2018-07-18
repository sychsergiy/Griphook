import click
from tabulate import tabulate

from griphook.cli.utils import sql_utils, data_utils

CUSTOM_DATE = data_utils.CustomDateParamType()


# process == services_group
@click.command()
@click.argument('process', type=click.Choice(['prom-madmax', 'prom-furiosa',
                                                'prom--by-trunk', 'bigl-rabbit-stable',
                                                'bigl-rabbit-default', 'bigl-duty-schedule']))
@click.option('--mtype',
              type=click.Choice(['user_cpu_percent',
                                 'vsize', 'system_cpu_percent']),
              default='system_cpu_percent',
              help="What type of metrics would you like to get?")
@click.option('--period',  type=(CUSTOM_DATE, CUSTOM_DATE), help="Provide the period.")
# @click.option('--hours',  type=int, default=1, help="For the period of how many hours?")
def grip(process, mtype, period):
    """Simple CLI  utillity to print metrics."""
    metrics = sql_utils.make_query(process, mtype, period)
    click.echo(tabulate(data_utils.metric_data(metrics), headers="keys", tablefmt="fancy_grid"))


if __name__ == '__main__':
    grip()
