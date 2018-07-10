import os
import trafaret
import unittest
import yaml

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
        os.remove(self.FILE_NAME)

    def write_yml_config(self, data):
        with open(self.FILE_NAME, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

    def remove_config_file(self):
        os.remove(self.FILE_NAME)

    def test_correct_config(self):
        data = {
            "api": "value",
            "cli": "value",
            "tasks": "value",
            "db": "value",
        }
        self.write_yml_config(data)

        config = Config(self.test_template).config
        self.assertEqual(config, data)

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

        config = Config().config
        self.assertEqual(config, data)


if __name__ == '__main__':
    unittest.main()
