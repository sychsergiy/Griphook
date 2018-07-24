import os
import pathlib
import sys

import trafaret
import yaml

from griphook.config.template import template as default_template

BASE_DIR = pathlib.Path(__file__).parents[2]

DEFAULT_CONFIG_FILE_NAME = 'config.yml'
DEFAULT_PREFIX = "GH_"


class Config(object):
    def __init__(self, template: trafaret.base.Dict = default_template,
                 prefix=DEFAULT_PREFIX) -> None:
        self.prefix = prefix

        config_file_name = os.environ.get(self.prefix + "CONFIG_FILE_NAME", DEFAULT_CONFIG_FILE_NAME)
        self.config_file_path = os.path.join(BASE_DIR, config_file_name)

        self.template = template
        self._options = self.read_options_from_config_file()
        self.override_options_from_environ(self._options)
        self.validate_options(self._options)

    def read_options_from_config_file(self) -> dict:
        """
        Read options from YML file
        exit with code 1 if configuration file doesn't exist
        :return: parsed dict
        """
        try:
            with open(self.config_file_path) as stream:
                return yaml.safe_load(stream)
        except FileNotFoundError:
            error_message = "No such file {}. Provide GH_DEFAULT_CONFIG_FILE_NAME env variable or create file".format(
                self.config_file_path)
            sys.stderr.write(error_message)
            sys.exit(1)

    @property
    def options(self) -> dict:
        return self._options

    def override_options_from_environ(self, option_dict) -> None:
        """
        Recursively check options dict.
        If option is nested dict call this function with nested_dict as argument
        Else option is primitive, so just check if environment variable with the same (PREFIX + name),
         overwrite if yes.
        """
        for key, value in option_dict.items():
            if isinstance(value, dict):
                self.override_options_from_environ(value)
            else:
                env_variable = os.environ.get(self.prefix + key)
                if env_variable:
                    option_dict[key] = env_variable

    def validate_options(self, options):
        """
        Validate options with trafaret template
        with code 1 and print errors to stderr
        """
        try:
            self.template.check(options)
        except trafaret.DataError as e:
            sys.stderr.write(str(e) + "\n")
            sys.exit(1)
