import sys
import os
import trafaret

from trafaret_config import read_and_validate, ConfigError

from template import template as default_template

DEFAULT_CONFIG_PATH = '/config.yml'
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # todo: find better way to get root dir path

CONFIG_PATH = BASE_DIR + os.environ.get("CONFIG_PATH", DEFAULT_CONFIG_PATH)

PREFIX = "GH_"


class Config(object):
    def __init__(self, template: trafaret.base.Dict = default_template):
        try:
            self._options = read_and_validate(CONFIG_PATH, template)
            self.override_options_from_environ()
            template.check(self._options)
        except ConfigError as e:
            e.output()
            sys.exit(1)
        except FileNotFoundError:
            error_message = "No such file {}. Provide CONFIG_PATH env variable or create file".format(CONFIG_PATH)
            print(error_message)
            sys.exit(1)

    @property
    def options(self) -> dict:
        return self._options

    def override_options_from_environ(self):
        """
        For every options group (tasks, db, general) check
        if environ variables with the same name and GH_ prefix exists overwrite option
            yes: overwrite option

        """
        for key, value in self._options.items():
            if isinstance(value, dict):
                for nested_key in value:
                    environ_variable = os.environ.get(PREFIX + nested_key)
                    if environ_variable:
                        self._options[key][nested_key] = environ_variable


if __name__ == "__main__":
    config = Config()
    print(config.options)
