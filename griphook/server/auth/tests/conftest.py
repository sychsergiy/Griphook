import pytest

from griphook.server.models import Admin
from griphook.tests.base_fixtures import app, client, client_class


@pytest.fixture
def admin_password():
    return "admin_password"


@pytest.fixture
def default_admin(admin_password):
    return Admin(password=admin_password)
