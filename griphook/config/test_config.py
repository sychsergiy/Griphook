import os
import trafaret
import unittest
import yaml

from unittest import mock

from trafaret_config import ConfigError

from config import Config, BASE_DIR


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.FILE_NAME = BASE_DIR + '/config.yml'

        self.test_template = trafaret.Dict({
            'api': trafaret.String(),
            'cli': trafaret.String(),
            'db': trafaret.String(),
            'tasks': trafaret.String(),
        })

    def tearDown(self):
        try:
            os.remove(self.FILE_NAME)
        except FileNotFoundError:
            pass

    def write_yml_config(self, data):
        with open(self.FILE_NAME, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

    def test_correct_config(self):
        data = {
            "api": "value",
            "cli": "value",
            "tasks": "value",
            "db": "value",
        }
        self.write_yml_config(data)

        options = Config(self.test_template).options
        self.assertEqual(options, data)

    def test_wrong_config(self):
        data = {
            "api": "value",
            "cli": "value",
            "tasks": 1,
            "db": "value",
        }
        self.write_yml_config(data)

        with self.assertRaises(SystemExit):
            with self.assertRaises(ConfigError):
                Config(self.test_template)

    def test_current_config(self):
        data = {
            "api": "value",
            "cli": "value",
            "db": "value",
            "tasks": {
                "DATA_SOURCE_DATA_EXPIRES": "test",
                "CELERY_BROKER_URL": "test",
                "TRYING_SETUP_PARSER_INTERVAL": 1,
                "PARSE_METRIC_EXPIRES": 1,
            },
        }
        self.write_yml_config(data)

        options = Config().options
        self.assertEqual(options, data)

    def test_overwriting_options_from_env(self):
        data = {
            "api": "value",
            "cli": "value",
            "db": "value",
            "tasks": {
                "DATA_SOURCE_DATA_EXPIRES": "test",
                "CELERY_BROKER_URL": "test",
                "TRYING_SETUP_PARSER_INTERVAL": 1,
                "PARSE_METRIC_EXPIRES": 1,
            },
        }

        self.write_yml_config(data)
        data['tasks']['DATA_SOURCE_DATA_EXPIRES'] = 'new_value'

        os.environ['GH_DATA_SOURCE_DATA_EXPIRES'] = "new_value"
        config = Config()

        self.assertEqual(config.options, data)


if __name__ == '__main__':
    unittest.main()
