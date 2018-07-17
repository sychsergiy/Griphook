import click
from tabulate import tabulate

from griphook.cli.utils import make_query, metric_data


# process == services_group
@click.command()
@click.argument('process', type=click.Choice(['prom-madmax', 'prom-furiosa',
                                                'prom--by-trunk', 'bigl-rabbit-stable',
                                                'bigl-rabbit-default', 'bigl-duty-schedule']))
@click.option('--type',
              type=click.Choice(['user_cpu_percent',
                                 'vsize', 'system_cpu_percent']),
              default='system_cpu_percent',
              help="What type of metrics would you like to get?")
@click.option('--days',  type=int, default=0, help="For the period of how many days?")
@click.option('--hours',  type=int, default=1, help="For the period of how many hours?")
def griphook(process, type, hours, days):
    """Simple CLI  utillity to print metrics."""
    metrics = make_query(process, type, days, hours)
    click.echo(tabulate(metric_data(metrics), headers="keys", tablefmt="fancy_grid"))


if __name__ == '__main__':
    griphook()
