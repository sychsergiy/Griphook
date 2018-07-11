import os
import yaml
import trafaret
import unittest

from trafaret_config import ConfigError

from config import Config, BASE_DIR


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.FILE_NAME = BASE_DIR + "/config.yml"

        self.test_template = trafaret.Dict({
            "api": trafaret.String(),
            "cli": trafaret.String(),
            "db": trafaret.String(),
            "tasks": trafaret.String(),
        })

        self.current_config_data = {
            "api": {
                "GRAPHITE_URL": "url_here"
            },
            "db": {
                "DATABASE_URL": "url here"
            },
            "tasks": {
                "DATA_SOURCE_DATA_EXPIRES": "test",
                "CELERY_BROKER_URL": "test",
                "BROKER_DATABASE_URL": "url here",
                "TRYING_SETUP_PARSER_INTERVAL": 1,
                "PARSE_METRIC_EXPIRES": 1,
            },
        }

    def tearDown(self):
        os.remove(self.FILE_NAME)

    def write_yml_config(self, data):
        with open(self.FILE_NAME, "w") as file:
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
        data = self.current_config_data

        self.write_yml_config(data)

        options = Config().options
        self.assertEqual(options, data)

    def test_overwriting_options_from_env_of_current_template(self):
        data = self.current_config_data

        self.write_yml_config(data)
        data["tasks"]["DATA_SOURCE_DATA_EXPIRES"] = "new_value"

        os.environ["GH_DATA_SOURCE_DATA_EXPIRES"] = "new_value"
        config = Config()

        self.assertEqual(config.options, data)

    def test_overwriting_by_env_variable_with_wrong_type(self):
        data = self.current_config_data
        self.write_yml_config(data)

        os.environ["GH_PARSE_METRIC_EXPIRES"] = "string here"  # set wrong data type

        with self.assertRaises(SystemExit):
            with self.assertRaises(trafaret.DataError):
                Config()

        os.environ.pop("GH_PARSE_METRIC_EXPIRES", None)


if __name__ == "__main__":
    unittest.main()
