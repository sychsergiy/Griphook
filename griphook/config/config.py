import sys
import os

from trafaret_config import read_and_validate, ConfigError

from template import CONFIG_TEMPLATE

DEFAULT_CONFIG_PATH = '/config.yaml'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_PATH = BASE_DIR + os.environ.get("CONFIG_PATH", DEFAULT_CONFIG_PATH)


def get_config():
    try:
        return read_and_validate(CONFIG_PATH, CONFIG_TEMPLATE)
    except ConfigError as e:
        e.output()
        sys.exit(1)
    except FileNotFoundError:
        error_message = "No such file {}. Provide CONFIG_PATH env variable or create file".format(CONFIG_PATH)
        print(error_message)
        sys.exit(1)
