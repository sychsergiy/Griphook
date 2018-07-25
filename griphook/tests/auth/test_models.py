import datetime

from griphook.tests.common.base import BaseTestCase
from griphook.server.auth.models import User


class UserModelTestCase(BaseTestCase):
    def test_registered_on_defaults_to_datetime(self):
        # Ensure that registered_on is a datetime.
        with self.client:
            self.client.post('/login', data=dict(
                email='ad@min.com', password='admin_user'
            ), follow_redirects=True)
            user = User.query.filter_by(email='ad@min.com').first()
            self.assertIsInstance(user.registered_on, datetime.datetime)
