from griphook.server import db
from griphook.tests.base import BaseTestCase


class BaseWithDBSession(BaseTestCase):

    def setUp(self):
        super(BaseWithDBSession, self).setUp()
        self.session = db.session
