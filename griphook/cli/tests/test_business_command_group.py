import unittest

from click.testing import CliRunner

from griphook.cli.business import cli


class BusinessCommandGroupTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.runner = CliRunner()

    def test_create_team_command(self):
        result = self.runner.invoke(cli, ['create_team', 'test'])
        self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()
