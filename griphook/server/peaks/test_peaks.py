from griphook.server import db
from griphook.tests.base import BaseTestCase


class BaseWithDBSession(BaseTestCase):

    def setUp(self):
        super(BaseWithDBSession, self).setUp()
        self.session = db.session
        self.app = self.create_app()
        self.client = self.app.test_client()

    def test_server_peak(self):
        response = self.client.get('/peaks/peaks', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
