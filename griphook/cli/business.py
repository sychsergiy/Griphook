import click

from griphook.cli.utils.db_utils import get_session_class
from griphook.cli.managers.team import TeamManager
from griphook.cli.managers.project import ProjectManager

Session = get_session_class()


# todo: handle ManagerException

@click.group()
@click.pass_context
def cli(ctx):
    if ctx.obj is None:
        ctx.obj = {}
    session = Session()
    ctx.obj['team_manager'] = TeamManager(session)
    ctx.obj['project_manager'] = ProjectManager(session)


@cli.command()
@click.argument('title', type=click.STRING)
@click.pass_context
def create_team(ctx, title):
    ctx.obj['team_manager'].create(title=title)


@cli.command()
@click.argument('title', type=click.STRING)
@click.pass_context
def create_project(context, title):
    context.obj['project_manager'].create(title=title)


@cli.command()
@click.argument('service_group_title', type=click.STRING)
@click.argument('project_title', type=click.STRING)
@click.pass_context
def attach_process_to_project(ctx, service_group_title, project_title):
    ctx.obj['project_manager'].attach_to_service_group(service_group_title, project_title)


@cli.command()
@click.argument('service_group_title', type=click.STRING)
@click.argument('team_title', type=click.STRING)
@click.pass_context
def attach_process_to_team(ctx, service_group_title, team_title):
    ctx.obj['team_manager'].attach_to_service_group(service_group_title, team_title)


if __name__ == "__main__":
    cli()
