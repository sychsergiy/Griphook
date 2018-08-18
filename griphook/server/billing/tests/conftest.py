import pytest

from griphook.server import create_app
from griphook.server import db as _db


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object("griphook.server.config.TestingConfig")
    return app


@pytest.fixture
def session(app):
    session = _db.session
    # _db.drop_all()
    # _db.create_all()
    session.commit()
    yield session
