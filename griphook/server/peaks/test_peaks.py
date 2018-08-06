from datetime import datetime, timedelta
import json

from flask import url_for

from griphook.server import db
from griphook.tests.base import BaseTestCase
from griphook.server.models import Metric, BatchStory, Service, ServicesGroup


class BaseWithDBSession(BaseTestCase):

    def setUp(self):
        super(BaseWithDBSession, self).setUp()
        self.session = db.session
        self.app = self.create_app()
        self.client = self.app.test_client()

        service_group1 = ServicesGroup(title="group1")
        service_group2 = ServicesGroup(title="group2")
        self.session.add_all([service_group1, service_group2])
        service1 = Service(title="service1", server="test1", services_group=service_group1)
        service2 = Service(title="service2", server="test1", services_group=service_group2)
        service3 = Service(title="service3", server="test2", services_group=service_group2)
        self.session.add_all([service1, service2, service3])
        self.time1 = datetime.now() - timedelta(days=8)
        self.time2 = datetime.now()
        batches_story1 = BatchStory(time=self.time1)
        batches_story2 = BatchStory(time=self.time2)
        self.session.add_all([batches_story1, batches_story2])
        metric1 = Metric(
            value=2,
            batch=batches_story1,
            service=service1,
            services_group=service_group1,
            type='user_cpu_percent'
        )
        metric2 = Metric(
            value=2,
            batch=batches_story2,
            service=service2,
            services_group=service_group2,
            type='user_cpu_percent'
        )
        metric3 = Metric(
            value=3,
            batch=batches_story2,
            service=service3,
            services_group=service_group2,
            type='user_cpu_percent'
        )
        metric4 = Metric(
            value=4,
            batch=batches_story1,
            service=service3,
            services_group=service_group2,
            type='user_cpu_percent'
        )
        self.session.add_all([metric1, metric2, metric3, metric4])
        self.week = 604800

    def test_server_peak_data_validation(self):
        url = url_for('peaks.peaks-api')
        data = {
            'server': 'test1',
            'metric_type': "user_cpu_percent",
            'step': self.week,
            "since": self.time1.strftime('%Y-%m-%d'),
            "until": self.time2.strftime('%Y-%m-%d')
        }

        for key in data:
            response = self.request_without_ruquied_field(self.client, url, data, key)
            self.assertEqual(response.status_code, 400)

        response = self.client.get(url, query_string=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_peaks_query(self):
        url = url_for('peaks.peaks-api')
        data = {
            'server': 'test2',
            'metric_type': "user_cpu_percent",
            'step': self.week,
            "since": self.time1.strftime('%Y-%m-%d'),
            "until": self.time2.strftime('%Y-%m-%d')
        }
        response = self.client.get(url, query_string=data, follow_redirects=True)
        resp_data = json.loads(response.data.decode('utf-8'))['data']
        self.assertEqual(len(resp_data), 2)
        self.assertEqual(resp_data[0][1], self.time1.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(resp_data[1][1], self.time2.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(resp_data[0][0], 4)
        self.assertEqual(resp_data[1][0], 3)

        data['server'] = 'test1'
        response = self.client.get(url, query_string=data, follow_redirects=True)
        resp_data = json.loads(response.data.decode('utf-8'))['data']
        self.assertEqual(len(resp_data), 2)
        self.assertEqual(resp_data[0][1], self.time1.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(resp_data[1][1], self.time2.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(resp_data[0][0], 2)
        self.assertEqual(resp_data[1][0], 2)

        data['step'] = self.week * 4
        response = self.client.get(url, query_string=data, follow_redirects=True)
        resp_data = json.loads(response.data.decode('utf-8'))['data']
        self.assertEqual(len(resp_data), 1)
        self.assertEqual(resp_data[0][1], self.time1.strftime('%Y-%m-%d %H:%M:%S'))


    @staticmethod
    def request_without_ruquied_field(client, url, data, field):
        value = data[field]
        data.pop(field)
        response = client.get(url, query_string=data, follow_redirects=True)
        data[field] = value
        return response
