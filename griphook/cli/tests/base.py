import unittest

from griphook.cli.managers.base import get_session_class
from server.models import Project, ServicesGroup, Team

Session = get_session_class()


class BaseWithDBSession(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = Session()

    @classmethod
    def tearDownClass(cls):
        cls.clean_up_db()
        cls.session.close()

    @classmethod
    def clean_up_db(cls):
        cls.session.query(ServicesGroup).delete()
        cls.session.query(Project).delete()
        cls.session.query(Team).delete()
        cls.session.commit()
