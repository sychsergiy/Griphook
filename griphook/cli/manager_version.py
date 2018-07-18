from contextlib import contextmanager, ContextDecorator

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from griphook.config.config import Config
from griphook.db.models import Team


def get_session_class():
    config = Config()
    db_url = config.options["db"]["DATABASE_URL"]
    engine = create_engine(db_url)
    return sessionmaker(bind=engine)


Session = get_session_class()


# ----------------------------------------------------------------------------
@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class ManagerWithClosingSession(object):

    def create_team(self, title):
        with session_scope() as session:
            instance = Team(title=title)
            session.add(instance)


# ----------------------------------------------------------------------------

class ManagerContextManager(object):
    def __enter__(self):
        self.session = Session()
        return self

    def create_team(self, title):
        instance = Team(title=title)
        self.session.add(instance)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


# -----------------------------------------------------------------------------


class session_scope_context_manager(ContextDecorator):
    def __enter__(self):
        self.session = Session()
        return self

    def __exit__(self, *exc):
        self.session.commit()
        self.session.close()
        return False


class ManagerWithDecoratedMethods(object):
    @session_scope_context_manager()
    def create_team(self, title):
        instance = Team(title=title)
        self.session.add(instance)
        return instance
