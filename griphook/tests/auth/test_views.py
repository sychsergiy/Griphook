import base64

from flask import url_for
from flask_login import current_user

from griphook.tests.common.base import BaseTestCase

from griphook.server.auth.models import User


class LoginViewTestCase(BaseTestCase):
    def test_correct_login(self):
        # Ensure login behaves correctly with correct credentials.
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="ad@min.com", password="admin_user"),
            )
            self.assertTrue(current_user.is_active)
            self.assertRedirects(response, url_for('auth.members'))
            self.assertEqual(current_user.email, 'ad@min.com')

    def test_get_by_id(self):
        # Ensure id is correct for the current/logged in auth.
        with self.client:
            self.client.post('/login', data=dict(
                email='ad@min.com', password='admin_user'
            ), follow_redirects=True)
            user = User.query.filter(User.email == 'ad@min.com').first()
            self.assertTrue(current_user.id == user.id)

    def test_validate_invalid_password(self):
        # Ensure auth can't login when the password is incorrect.
        with self.client:
            response = self.client.post('/login', data=dict(
                email='ad@min.com', password='foo_bar'
            ), follow_redirects=True)
        self.assertIn(b'Invalid email and/or password.', response.data)


class LogoutViewTestCase(BaseTestCase):
    def test_logout_route_requires_login(self):
        # Ensure logout route requires logged in auth.
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

    def test_logout_behaves_correctly(self):
        # Ensure logout behaves correctly - regarding the session.
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="ad@min.com", password="admin_user"),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You were logged out. Bye!', response.data)
            self.assertFalse(current_user.is_active)


class MemberViewTestCase(BaseTestCase):
    def test_member_route_requires_login(self):
        # Ensure member route requires logged in auth.
        response = self.client.get('/members')
        '/login?next=%2Fmembers'
        self.assertRedirects(response, url_for('auth.login', next='/members'))

    def test_view_return_200_status_code_and_use_correct_template(self):
        # todo: how to login user
        response = self.client.get('/members')
        # self.assert200(response)
        # self.assertTemplateUsed('auth/members.html')


class RegisterViewTestCase(BaseTestCase):
    def test_view_return_200_status_code_and_use_correct_template(self):
        # Ensure about route behaves correctly.
        response = self.client.get('/register', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('auth/register.html')

    def test_user_registration(self):
        # Ensure registration behaves correctly.
        with self.client:
            response = self.client.post(
                '/register',
                data=dict(email="test@tester.com", password="testing",
                          confirm="testing"),
                follow_redirects=True
            )
            self.assertIn(b'Welcome', response.data)
            self.assertTrue(current_user.email == "test@tester.com")
            self.assertTrue(current_user.is_active())
            self.assert200(response)
