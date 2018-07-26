from flask import url_for

from griphook.server import db
from griphook.tests.common.base import BaseTestCase
from griphook.server.models import Service, ServicesGroup


class ServersAPIViewTestCase(BaseTestCase):
    def test_view_return_correct_response(self):
        db.session.add_all([
            Service(title='test', server='test1'), Service(title='test1', server='test1'),
            Service(title='test2', server='test'), Service(title='test3', server='test2'),
            Service(title='test4', server='test3'), Service(title='test6', server='test'),
        ])

        expected_response_data = ['test', 'test1', 'test2', 'test3']
        response = self.client.get('/filters/servers')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), expected_response_data)


class ServiceGroupsAPIViewTestCase(BaseTestCase):
    def test_view_return_correct_response(self):
        sv_group1 = ServicesGroup(title='service_group_1')
        sv_group2 = ServicesGroup(title='service_group_2')
        sv_group3 = ServicesGroup(title='service_group_3')
        db.session.add_all([
            sv_group1, sv_group2, sv_group3,
            Service(title='service', server='server1', services_group=sv_group1),
            Service(title='service', server='server1', services_group=sv_group2),
            Service(title='service2', server='server2'), Service(title='service', server='server3'),
        ])
        db.session.commit()

        expected_response = ['service_group_1', 'service_group_2']

        response = self.client.get(url_for('filters.service_groups', server_title='server1'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), expected_response)


class ServicesAPIViewTestCase(BaseTestCase):
    def test_view_return_correct_response(self):
        sv_group1 = ServicesGroup(title='service_group_1')
        sv_group2 = ServicesGroup(title='service_group_2')

        db.session.add_all([
            sv_group1, sv_group2,
            Service(title='service1', services_group=sv_group1),
            Service(title='service2', services_group=sv_group1),
            Service(title='service3', services_group=sv_group2),
            Service(title='service4', ),
        ])
        expected_data = ['service1', 'service2']

        response = self.client.get(url_for('filters.services', services_group_title='service_group_1'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), expected_data)
