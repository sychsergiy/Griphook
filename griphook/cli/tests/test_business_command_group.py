import unittest

from click.testing import CliRunner

from griphook.cli.business import cli
from griphook.db.models import ServicesGroup, Project, Team
from griphook.cli.tests.base import BaseWithDBSession


class BusinessCommandGroupTestCase(BaseWithDBSession):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.runner = CliRunner()

    def setUp(self):
        self.clean_up_db()

    def test_create_team_command(self):
        result = self.runner.invoke(cli, ['create_team', 'test'])

        self.assertEqual(result.exit_code, 0)

    def test_create_project_command(self):
        result = self.runner.invoke(cli, ['create_project', 'test'])
        self.assertEqual(result.exit_code, 0)

    def test_attach_process_to_project_command(self):
        self.session.add_all([ServicesGroup(title='test'), Project(title='test')])
        self.session.commit()

        result = self.runner.invoke(cli, ['attach_process_to_project', 'test', 'test'])
        self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()
