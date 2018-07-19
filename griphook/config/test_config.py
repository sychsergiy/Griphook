import os
import unittest
from unittest import mock

import trafaret
import yaml

from griphook.config.config import BASE_DIR, Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.PREFIX = "TEST_GH_"
        self.CONFIG_FILE_PATH = os.path.join(BASE_DIR, "config.yml")

        self.test_template = trafaret.Dict({
            "api": trafaret.String(),
            "cli": trafaret.String(),
            "tasks": trafaret.String(),
            "db": trafaret.Dict({
                "DATABASE_URL": trafaret.String(),
                "EXPIRES_TIME": trafaret.Int(),
            }),

        })
        self.test_data = {
            "api": "value",
            "cli": "value",
            "tasks": "value",
            "db": {
                "DATABASE_URL": "URL",
                "EXPIRES_TIME": 1,
            },
        }

        self.current_config_data = {
            "api": {
                "GRAPHITE_URL": "url_here"
            },
            "db": {
                "DATABASE_URL": "url here"
            },
            "tasks": {
                "DATA_SOURCE_DATA_EXPIRES": 1,
                "CELERY_BROKER_URL": "test",
                "TRYING_SETUP_PARSER_INTERVAL": 1,
                "PARSE_METRIC_EXPIRES": 1,
                "DATA_GRANULATION": 1,
            },
        }

    def tearDown(self):
        os.remove(self.CONFIG_FILE_PATH)

    def write_yml_config(self, data):
        with open(self.CONFIG_FILE_PATH, "w") as file:
            yaml.dump(data, file, default_flow_style=False)

    def test_correct_config(self):
        data = self.test_data
        self.write_yml_config(data)

        options = Config(self.test_template, prefix=self.PREFIX).options
        self.assertEqual(options, data)

    def test_wrong_config_data(self):
        data = {
            "api": "value",
            "cli": "value",
            "tasks": 1,
            "db": {
                "DATABASE_URL": "URL",
                "EXPIRES_TIME": 1,
            },
        }
        self.write_yml_config(data)

        with self.assertRaises(SystemExit):
            with self.assertRaises(trafaret.DataError):
                Config(self.test_template, prefix=self.PREFIX)

    def test_current_config(self):
        data = self.current_config_data

        self.write_yml_config(data)

        options = Config(prefix=self.PREFIX).options
        self.assertEqual(options, data)

    @mock.patch.dict(os.environ, {"TEST_GH_CELERY_BROKER_URL": "new_value"})
    def test_overwriting_options_from_env_of_current_template(self):
        data = self.current_config_data

        self.write_yml_config(data)
        data["tasks"]["CELERY_BROKER_URL"] = "new_value"

        config = Config(prefix=self.PREFIX)
        self.assertEqual(config.options, data)

    @mock.patch.dict(os.environ, {'TEST_GH_EXPIRES_TIME': 'str'})
    def test_overwriting_by_env_variable_with_wrong_type(self):
        data = self.test_data
        self.write_yml_config(data)

        with self.assertRaises(SystemExit):
            with self.assertRaises(trafaret.DataError):
                Config(self.test_template, prefix=self.PREFIX)

    @mock.patch.dict(os.environ, {'TEST_GH_TOP_LEVEL_VARIABLE': '2',
                                  'TEST_GH_NESTED_DICT': "test",
                                  'TEST_GH_SOURCE_DATA_EXPIRES': '2'})
    def test_override_options_from_environ_method_with_nested_dict(self):
        data = {
            "TOP_LEVEL_VARIABLE": 1,
            "NESTED_DICT": {
                "SOURCE_DATA_EXPIRES": 1,
            }
        }
        self.write_yml_config(data)

        template = trafaret.Dict({
            "TOP_LEVEL_VARIABLE": trafaret.Int(),
            "NESTED_DICT": trafaret.Dict({
                "SOURCE_DATA_EXPIRES": trafaret.Int(),
            })
        })

        expected_data = {
            "TOP_LEVEL_VARIABLE": '2',
            "NESTED_DICT": {
                "SOURCE_DATA_EXPIRES": '2',
            }
        }
        config = Config(template, prefix=self.PREFIX)
        self.assertEqual(config.options, expected_data)


if __name__ == "__main__":
    unittest.main()
