from flask import url_for

from griphook.tests.base import BaseTestCase


class ServerAverageLoadViewTestCase(BaseTestCase):
    def test_view_return_400_status_code_if_server_title_argument_not_given(self):
        response = self.client.get(url_for('average_load.server'))
        self.assert400(response)
        response = self.client.get(url_for('average_load.server', time_from=1524873600))
        self.assert400(response)
        response = self.client.get(url_for('average_load.server', time_until=1524897199))
        self.assert400(response)

    def test_view_return_405_status_on_post_with_wrong_arguments(self):
        response = self.client.post(url_for('average_load.server'))
        self.assert405(response)

    def test_view_return_200_status_code(self):
        params = {
            'time_from': 1524873600,
            'time_until': 1524897199,
            'metric_type': 'vsize',
            'server': 'bart',
        }
        response = self.client.get(url_for('average_load.server', **params))
        self.assert200(response)


class ServicesGroupAverageViewTestCase(BaseTestCase):

    def test_view_return_400_status_code_if_wrong_arguments_given(self):
        response = self.client.get(url_for('average_load.services_group'))
        self.assert400(response)
        response = self.client.get(url_for('average_load.services_group', time_from=1524873600))
        self.assert400(response)
        response = self.client.get(url_for('average_load.services_group', time_until=1524897199))
        self.assert400(response)

    def test_view_return_405_status_on_post_with_wrong_arguments(self):
        response = self.client.post(url_for('average_load.services_group'))
        self.assert405(response)

    def test_view_return_200_status_code(self):
        params = {
            'time_from': 1524873600,
            'time_until': 1524897199,
            'metric_type': 'vsize',
            'services_group': 'adv-stable',
        }
        response = self.client.get(url_for('average_load.services_group', **params))
        self.assert200(response)


class ServiceAverageViewTestCase(BaseTestCase):
    def test_view_return_400_status_code_if_wrong_arguments_give(self):
        response = self.client.get(url_for('average_load.service'))
        self.assert400(response)
        response = self.client.get(url_for('average_load.service', time_from=1524873600))
        self.assert400(response)
        response = self.client.get(url_for('average_load.service', time_until=1524897199))
        self.assert400(response)

    def test_view_return_405_status_on_post_with_wrong_arguments(self):
        response = self.client.post(url_for('average_load.service'))
        self.assert405(response)

    def test_view_return_200_status_code(self):
        params = {
            'time_from': 1524873600,
            'time_until': 1524897199,
            'metric_type': 'vsize',
            'service': 'site-bigl',
        }
        response = self.client.get(url_for('average_load.service', **params))
        self.assert200(response)
