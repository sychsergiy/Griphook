import click

from griphook.cli.manager import Manager, get_session_class

Session = get_session_class()


# todo: handle ManagerException
# todo: add test for every edge situations after handling ManagerException

@click.group()
@click.pass_context
def cli(ctx):
    if ctx.obj is None:
        ctx.obj = {}
    ctx.obj['manager'] = Manager(Session())


@cli.command()
@click.argument('title', type=click.STRING)
@click.pass_context
def create_team(ctx, title):
    ctx.obj['manager'].create_team(title=title)


@cli.command()
@click.argument('title', type=click.STRING)
@click.pass_context
def create_project(context, title):
    context.obj['manager'].create_project(title=title)


@cli.command()
@click.argument('service_group_title', type=click.STRING)
@click.argument('project_title', type=click.STRING)
@click.pass_context
def attach_process_to_project(ctx, project_title, service_group_title):
    ctx.obj['manager'].attach_service_group_to_project(service_group_title, project_title)


if __name__ == "__main__":
    cli()
