import unittest

from griphook.cli.manager import get_session_class, Manager, ManagerException
from griphook.db.models import Team, Project

Session = get_session_class()


class ManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.clean_up_db()
        self.manager = Manager()

    @classmethod
    def setUpClass(cls):
        cls.session = Session()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def clean_up_db(self):
        self.session.query(Team).delete()
        self.session.query(Project).delete()
        self.session.commit()

    def test_create_team_method(self):
        title = 'test'
        self.manager.create_team(title=title)
        teams_quantity = self.session.query(Team).count()
        self.assertEqual(teams_quantity, 1)

    def test_create_two_teams_with_the_same_title(self):
        title = 'test'
        self.session.add(Team(title=title))
        self.session.commit()

        with self.assertRaises(ManagerException):
            self.manager.create_team(title=title)
            self.session.commit()

    def test_create_project_method(self):
        title = 'test'
        self.manager.create_project(title=title)
        projects_quantity = self.session.query(Project).count()
        self.assertEqual(projects_quantity, 1)

    def test_create_two_projects_with_the_same_title(self):
        title = 'test'
        self.session.add(Project(title=title))
        self.session.commit()

        with self.assertRaises(ManagerException):
            self.manager.create_team(title=title)
            self.session.commit()


if __name__ == "__main__":
    unittest.main()
