import unittest

from click.testing import CliRunner

from griphook.cli.business import cli
from griphook.db.models import ServicesGroup, Project, Team
from griphook.cli.tests.base import BaseWithDBSession


class BusinessCreateCommandsTestCase(BaseWithDBSession):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.runner = CliRunner()

    def setUp(self):
        self.clean_up_db()

    def test_create_team_command(self):
        result = self.runner.invoke(cli, ['create_team', 'test'])
        self.assertEqual(result.exit_code, 0)

    def test_create_team_command_when_team_with_the_same_title_already_exists(self):
        self.session.add(Team(title='test'))
        self.session.commit()

        result = self.runner.invoke(cli, ['create_team', 'test'])
        self.assertEqual(result.exit_code, -1)

    def test_create_project_command(self):
        result = self.runner.invoke(cli, ['create_project', 'test'])
        self.assertEqual(result.exit_code, 0)

    def test_create_project_command_when_project_with_the_same_title_already_exists(self):
        self.session.add(Project(title='test'))
        self.session.commit()

        result = self.runner.invoke(cli, ['create_project', 'test'])
        self.assertEqual(result.exit_code, -1)


class BusinessAttachProcessToProjectCommandTestCase(BaseWithDBSession):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.runner = CliRunner()

    def setUp(self):
        self.clean_up_db()

    def test_attach_process_to_project_command(self):
        self.session.add_all([ServicesGroup(title='test'), Project(title='test')])
        self.session.commit()

        result = self.runner.invoke(cli, ['attach_process_to_project', 'test', 'test'])
        self.assertEqual(result.exit_code, 0)

    def test_attach_process_to_project_command_when_services_group_doesnt_exists(self):
        self.session.add(Project(title='test'))
        self.session.commit()

        result = self.runner.invoke(cli, ['attach_process_to_project', 'test', 'test'])
        self.assertEqual(result.exit_code, -1)

    def test_attach_process_to_project_command_when_project_doesnt_exists(self):
        self.session.add(ServicesGroup(title='test'))
        self.session.commit()

        result = self.runner.invoke(cli, ['attach_process_to_project', 'test', 'test'])
        self.assertEqual(result.exit_code, -1)


class BusinessAttachProcessToTeamCommandTestCase(BaseWithDBSession):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.runner = CliRunner()

    def setUp(self):
        self.clean_up_db()

    def test_attach_process_to_team_command(self):
        self.session.add_all([ServicesGroup(title='test'), Team(title='test')])
        self.session.commit()

        result = self.runner.invoke(cli, ['attach_process_to_team', 'test', 'test'])
        self.assertEqual(result.exit_code, 0)

    def test_attach_process_to_team_command_when_services_group_doesnt_exists(self):
        self.session.add(Team(title='test'))
        self.session.commit()

        result = self.runner.invoke(cli, ['attach_process_to_team', 'test', 'test'])
        self.assertEqual(result.exit_code, -1)

    def test_attach_process_to_team_command_when_team_doesnt_exists(self):
        self.session.add(ServicesGroup(title='test'))
        self.session.commit()

        result = self.runner.invoke(cli, ['attach_process_to_team', 'test', 'test'])
        self.assertEqual(result.exit_code, -1)


if __name__ == "__main__":
    unittest.main()
