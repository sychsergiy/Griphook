import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from griphook.config import Config
from griphook.server.models import Project, ServicesGroup, Team


def get_session_class():
    config = Config()
    db_url = config.options["db"]["DATABASE_TEST_URL"]
    engine = create_engine(db_url)
    return sessionmaker(bind=engine)


Session = get_session_class()


class BaseWithDBSession(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # db.create_all()
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
