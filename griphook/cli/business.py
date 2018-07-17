import click
import datetime

from griphook.cli.mocks import Team, Project


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))


@cli.command()
@click.argument('title', type=click.STRING)
def create_team(title):
    # todo: add unique validation
    instance = Team(title=title, created=datetime.datetime.utcnow())


@cli.command()
@click.argument('title', type=click.STRING)
def create_project(title):
    # todo: add unique validation
    instance = Project(title=title, created=datetime.datetime.utcnow())


if __name__ == "__main__":
    cli()
