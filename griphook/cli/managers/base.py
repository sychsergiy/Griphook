from griphook.cli.utils.db_utils import get_session_class

Session = get_session_class()


class BaseManager(object):
    def __init__(self, session):
        self.session = session
