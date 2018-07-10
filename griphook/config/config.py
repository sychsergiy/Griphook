import sys
import os
import trafaret

from trafaret_config import read_and_validate, ConfigError

from template import template as default_template

DEFAULT_CONFIG_PATH = '/config.yml'
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # todo: find better way to get root dir path

CONFIG_PATH = BASE_DIR + os.environ.get("CONFIG_PATH", DEFAULT_CONFIG_PATH)


class Config(object):
    def __init__(self, template: trafaret.base.Dict = default_template):
        try:
            self._config = read_and_validate(CONFIG_PATH, template)
        except ConfigError as e:
            e.output()
            sys.exit(1)
        except FileNotFoundError:
            error_message = "No such file {}. Provide CONFIG_PATH env variable or create file".format(CONFIG_PATH)
            print(error_message)
            sys.exit(1)

    @property
    def config(self) -> trafaret.base.Dict:
        return self._config
