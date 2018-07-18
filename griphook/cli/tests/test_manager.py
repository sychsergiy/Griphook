import unittest

from griphook.cli.manager import get_session_class, Manager
from griphook.db.models import Team

Session = get_session_class()


class ManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.manager = Manager()

    def tearDown(self):
        self.clean_up_db()

    @classmethod
    def setUpClass(cls):
        cls.session = Session()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def clean_up_db(self):
        self.session.query(Team).delete()
        self.session.commit()

    def test_create_team_method(self):
        title = 'test2'

        self.manager.create_team(title=title)
        teams_quantity = self.session.query(Team).count()
        self.assertEqual(teams_quantity, 1)


if __name__ == "__main__":
    unittest.main()
