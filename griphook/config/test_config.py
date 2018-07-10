import os

import unittest

from trafaret_config import ConfigError

from config import Config, BASE_DIR
from template import template


class TestConfig(unittest.TestCase):
    FILE_PATH = BASE_DIR + '/config.yaml'
    expected_config = {
        "api": "value",
        "cli": "value",
        "tasks": "value",
        "db": "value",
    }

    def test_correct_config(self):
        with open(self.FILE_PATH, 'w') as file:
            file.write("api: value\n")
            file.write("cli: value\n")
            file.write("tasks: value\n")
            file.write("db: value\n")
        config = Config().config

        self.assertEqual(config, self.expected_config)
        os.remove(self.FILE_PATH)

    def test_correct_config_with_default_template(self):
        with open(self.FILE_PATH, 'w') as file:
            file.write("api: value\n")
            file.write("cli: value\n")
            file.write("tasks: value\n")
            file.write("db: value\n")
        config = Config(template).config

        self.assertEqual(config, self.expected_config)
        os.remove(self.FILE_PATH)

    def test_wrong_config(self):
        with open(self.FILE_PATH, 'w') as file:
            file.write("api: value\n")
            file.write("cli: 1\n")
            file.write("tasks: value\n")
            file.write("db: value\n")

        with self.assertRaises(SystemExit):
            self.assertRaises(ConfigError, Config())
        os.remove(self.FILE_PATH)


if __name__ == '__main__':
    unittest.main()
