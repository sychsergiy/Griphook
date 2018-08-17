import subprocess

from flask.cli import FlaskGroup

from griphook.server import create_app, db
from griphook.server import models

# from griphook.tasks import task_scheduler


app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@cli.command()
def create_data():
    """Creates sample data."""
    pass


# @cli.command()
# @click.option(
#     '--celery_args',
#     type=str,
#     help='Additional parameters for celery, --app and worker already provided.'
# )
# def run_fetcher(celery_args):
#     """
#     Start both celery worker and task scheduler
#     """
#     celery_proc = subprocess.Popen([
#         'celery',
#         '--workdir=%s' % os.getcwd(),
#         '-A',
#         'griphook.tasks.tasks',
#         'worker',
#         *shlex.split(celery_args)
#     ])
#
#     task_scheduler.main()
#     celery_proc.wait()


@cli.command()
def flake():
    """Runs flake8 on the griphook."""
    exit_code = subprocess.run(['flake8', 'griphook']).returncode
    exit(exit_code)


if __name__ == '__main__':
    cli()
