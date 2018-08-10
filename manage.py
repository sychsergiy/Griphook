import os
import sys
import shlex
import subprocess
import click
import unittest
import coverage

from flask.cli import FlaskGroup

from griphook.server import create_app, db
from griphook.server import models
# from griphook.tasks import task_scheduler


app = create_app()
cli = FlaskGroup(create_app=create_app)

# code coverage
COV = coverage.coverage(
    branch=True,
    include='griphook/*',
    omit=[
        'griphook/tests/*',
        'griphook/server/config.py',
        'griphook/*/__init__.py'
    ]
)
COV.start()


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
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('griphook/', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('griphook/')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        sys.exit(0)
    else:
        sys.exit(1)


@cli.command()
def flake():
    """Runs flake8 on the griphook."""
    subprocess.run(['flake8', 'griphook'])


if __name__ == '__main__':
    cli()
