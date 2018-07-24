import click

from griphook.cli.utils.db_utils import get_session_class

Session = get_session_class()


class BaseManager(object):
    def __init__(self, session):
        self.session = session


class print_exception_message(object):
    def __init__(self, exception_class):
        self.exception_class = exception_class

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, traceback):

        if exc_type is not None:
            if issubclass(exc_type, self.exception_class):
                click.secho(str(exc_val), fg='red')
                return True
