import pytest

from griphook.server import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object('griphook.server.config.TestingConfig')
    return app
