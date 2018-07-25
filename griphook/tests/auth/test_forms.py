from griphook.tests.common.base import BaseTestCase
from griphook.server.auth.forms import LoginForm


class LoginFormTestCase(BaseTestCase):
    def test_validate_success_login_form(self):
        # Ensure correct data validates.
        form = LoginForm(email='ad@min.com', password='admin_user')
        self.assertTrue(form.validate())

    def test_validate_invalid_email_format(self):
        # Ensure invalid email format throws error.
        form = LoginForm(email='unknown', password='example')
        self.assertFalse(form.validate())


class RegisterFormTestCase(BaseTestCase):
    def test_correct_input_data(self):
        pass

    def test_incorrect_input_data_case1(self):
        pass

    def test_incorrect_input_data_case2(self):
        pass

    def test_incorrect_input_data_case3(self):
        pass
