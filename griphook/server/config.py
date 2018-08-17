# griphook/server/config.py

import os

from griphook.config import Config

options = Config().options

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = os.getenv("APP_NAME", "Flask Skeleton")
    BCRYPT_LOG_ROUNDS = 4
    DEBUG_TB_ENABLED = False
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = options["db"]["DATABASE_URL"]


class TestingConfig(BaseConfig):
    """Testing configuration."""

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = options["db"]["DATABASE_TEST_URL"]
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration."""

    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = options["db"]["DATABASE_URL"]
    WTF_CSRF_ENABLED = True
