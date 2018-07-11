import sys
import os
import trafaret

from trafaret_config import ConfigError, parse_and_validate

from template import template as default_template

DEFAULT_CONFIG_PATH = '/config.yml'
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # todo: find better way to get root dir path

CONFIG_PATH = BASE_DIR + os.environ.get("CONFIG_PATH", DEFAULT_CONFIG_PATH)

PREFIX = "GH_"


class Config(object):
    def __init__(self, template: trafaret.base.Dict = default_template):
        self.template = template
        self._options = self.read_and_validate_options_from_config_file()
        self.override_options_from_environ()
        self.validate_options()

    def read_and_validate_options_from_config_file(self) -> dict:
        """
        Read .yml file and validate  with trafaret template

        exit with code 1 if configuration file doesn't exist
        exit with code 1 if file has wrong configuration

        :return: parsed configuration from .yml file
        """
        with open(CONFIG_PATH) as f:
            text = f.read()
        try:
            return parse_and_validate(text, self.template, filename=CONFIG_PATH)
        except ConfigError as e:
            e.output()
            sys.exit(1)
        except FileNotFoundError:
            error_message = "No such file {}. Provide CONFIG_PATH env variable or create file".format(CONFIG_PATH)
            sys.stderr.write(error_message)
            sys.exit(1)

    @property
    def options(self) -> dict:
        return self._options

    def override_options_from_environ(self):
        """
        For every options group (tasks, db, general) check
        if environ variables with the same name and GH_ prefix exists
         overwrite option

        """
        for key, value in self._options.items():
            if isinstance(value, dict):
                for nested_key in value:
                    environ_variable = os.environ.get(PREFIX + nested_key)
                    if environ_variable:
                        self._options[key][nested_key] = environ_variable

    def validate_options(self):
        """
        Validate options with trafaret template
        with code 1 and print errors to stderr
        """
        try:
            self.template.check(self._options)
        except trafaret.DataError as e:
            sys.stderr.write(str(e) + "\n")
            sys.exit(1)


if __name__ == "__main__":
    config = Config()
    print(config.options)
