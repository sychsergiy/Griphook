import click

from griphook.cli.manager import Manager


@click.group()
@click.pass_context
def cli(context):
    context.obj['manager'] = Manager()


@cli.command()
@click.argument('title', type=click.STRING)
@click.pass_context
def create_team(context, title):
    context.obj['manager'].create_team(title=title)


if __name__ == "__main__":
    cli(obj={})
