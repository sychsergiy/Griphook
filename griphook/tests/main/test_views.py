from griphook.tests.common.base import BaseTestCase


class HomeViewTestCase(BaseTestCase):
    def test_view_return_200_status_code_and_use_correct_template(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertTemplateUsed('main/home.html')
        self.assert200(response)
