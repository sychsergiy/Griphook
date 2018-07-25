import pytest

from griphook.server import bcrypt
from griphook.tests.common.base import BaseTestCase
from griphook.server.auth.models import User


class UtilTestCase(BaseTestCase):
    def test_check_password_hash_function(self):
        user = User.query.filter_by(email='ad@min.com').first()

        self.assertTrue(bcrypt.check_password_hash(user.password, 'admin_user'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'foobar'))
