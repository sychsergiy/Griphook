import unittest

from cli.manager import get_session_class
from db.models import ServicesGroup, Project, Team

Session = get_session_class()


class BaseWithDBSession(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = Session()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        cls.clean_up_db()

    @classmethod
    def clean_up_db(cls):
        cls.session.query(ServicesGroup).delete()
        cls.session.query(Project).delete()
        cls.session.query(Team).delete()
        cls.session.commit()
