import pytest
from griphook.server.models import Admin


@pytest.fixture(autouse=True)
def get_admin_returns_default(admin_password, mocker):
    """
    Patch to avoid griphook.server.auth.utils.get_admin()
    performing requests to database (instead return Admin with admin_password)
    """
    mocker.patch(
        "griphook.server.auth.views.get_admin",
        return_value=Admin(password=admin_password),
    )


@pytest.mark.usefixtures("client_class")
class TestLoginView:
    def request(self, endpoint="auth/login", method="POST", *args, **kwargs):
        if method == "POST":
            return self.client.post(endpoint, *args, **kwargs)
        elif method == "GET":
            return self.client.get(endpoint, *args, **kwargs)
        raise NotImplementedError(f"Request with {method} method is invalid")

    def test_returns_token(self, admin_password):
        rv = self.request(json={"password": admin_password})
        assert rv.status_code == 200
        assert rv.json.get("access_token") is not None

    def test_wrong_password(self, admin_password):
        wrong_password = f"wrong_{admin_password}"
        rv = self.request(json={"password": wrong_password})
        assert rv.status_code == 401  # Unauthorized

    def test_get_request(self, admin_password):
        rv = self.request(json={"password": admin_password}, method="GET")
        assert rv.status_code == 405  # Method not allowed

    def test_no_password(self):
        rv = self.request(json={})
        assert rv.status_code == 400  # Bad request
