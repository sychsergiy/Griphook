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


@cli.command()
@click.argument('title', type=click.STRING)
@click.pass_context
def create_project(context, title):
    context.obj['manager'].create_project(title=title)


# @cli.commnad()
# @click.argument('service_group_title', type=click.STRING)
# @click.argument('project_title', type=click.STRING)
# @click.pass_context
# def attach_service_group_to_project(context, project_title, service_group_title):
#     context.obj['manager'].attach_service_group_to_project(project_title=project_title,
#                                                            service_group_title=service_group_title)


if __name__ == "__main__":
    cli(obj={})
