import pytest

from griphook.server.models import Admin
from griphook.tests.base_fixtures import app


@pytest.fixture
def admin_password():
    return "admin_password"


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def default_admin(admin_password):
    return Admin(password=admin_password)
