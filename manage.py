import subprocess
from getpass import getpass

from flask.cli import FlaskGroup

from griphook.server import create_app, db
from griphook.server.auth.exceptions import AdminExists
from griphook.server.auth.utils import create_admin, get_admin

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
    exit_code = subprocess.run(["flake8", "griphook"]).returncode
    exit(exit_code)


@cli.group(chain=True)
def admin():
    pass


@admin.command()
def create():
    """
    Create admin and set his password
    """
    try:
        create_admin(password=getpass())
    except AdminExists:
        print("Admin already exists")


@admin.command()
def set_password():
    """
    Set admin password
    """
    admin = get_admin()
    if not admin:
        print("Admin not exists")
        return

    try:
        admin.password = getpass()
    except ValueError as e:
        print(e)
    db.session.commit()


if __name__ == "__main__":
    cli()
