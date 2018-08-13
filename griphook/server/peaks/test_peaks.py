from datetime import datetime, timedelta
import json

from flask import url_for

from griphook.server import db
from griphook.tests.base import BaseTestCase
from griphook.server.models import MetricPeak, BatchStoryPeaks, Service, ServicesGroup, Server


class BaseWithDBSession(BaseTestCase):

    def setUp(self):
        super(BaseWithDBSession, self).setUp()
        self.session = db.session
        self.data_time_format = '%Y-%m-%d %H'

        service_group1 = ServicesGroup(title="group1")
        service_group2 = ServicesGroup(title="group2")
        self.session.add_all([service_group1, service_group2])
        self.session.commit()
        server1 = Server(title="test1")
        server2 = Server(title="test2")
        self.session.add_all([server1, server2])
        self.session.commit()
        service1 = Service(title="service1", instance='test', server_id=server1.id, services_group_id=service_group1.id)
        service2 = Service(title="service2", instance='test', server_id=server1.id, services_group_id=service_group2.id)
        service3 = Service(title="service3", instance='test', server_id=server2.id, services_group_id=service_group2.id)
        self.session.add_all([service1, service2, service3])
        self.session.commit()
        self.time1 = datetime.now() - timedelta(days=8)
        self.time2 = datetime.now()
        batches_story1 = BatchStoryPeaks(time=self.time1)
        batches_story2 = BatchStoryPeaks(time=self.time2)
        self.session.add_all([batches_story1, batches_story2])
        self.session.commit()
        metric1 = MetricPeak(
            value=2,
            batch_id=batches_story1.id,
            service_id=service1.id,
            services_group_id=service_group1.id,
            type='user_cpu_percent'
        )
        metric2 = MetricPeak(
            value=2,
            batch_id=batches_story2.id,
            service_id=service2.id,
            services_group_id=service_group2.id,
            type='user_cpu_percent'
        )
        metric3 = MetricPeak(
            value=3,
            batch_id=batches_story2.id,
            service_id=service3.id,
            services_group_id=service_group2.id,
            type='user_cpu_percent'
        )
        metric4 = MetricPeak(
            value=4,
            batch_id=batches_story1.id,
            service_id=service3.id,
            services_group_id=service_group2.id,
            type='user_cpu_percent'
        )
        self.session.add_all([metric1, metric2, metric3, metric4])
        self.session.commit()
        self.week = 604800

    def test_server_peak_data_validation(self):
        url = url_for('peaks.peaks-api')
        data = {
            'server': 'test1',
            'metric_type': "user_cpu_percent",
            'step': self.week,
            "time_from": self.time1.strftime(self.data_time_format),
            "time_until": self.time2.strftime(self.data_time_format)
        }

        for key in data:
            response = self.request_without_ruquied_field(self.client, url, data, key)
            self.assertEqual(response.status_code, 400)

        response = self.client.post(url, data=json.dumps(data), follow_redirects=True, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_peaks_query(self):
        url = url_for('peaks.peaks-api')
        data = {
            'server': 'test2',
            'metric_type': "user_cpu_percent",
            'step': self.week,
            "time_from": self.time1.strftime(self.data_time_format),
            "time_until": self.time2.strftime(self.data_time_format)
        }
        response = self.client.post(url, data=json.dumps(data), follow_redirects=True, content_type='application/json')
        resp_data = json.loads(response.data.decode('utf-8'))['data']
        self.assertEqual(len(resp_data['timeline']), 2)
        self.assertEqual(resp_data['timeline'][0], self.time1.strftime(self.data_time_format))
        self.assertEqual(resp_data['timeline'][1], self.time2.strftime(self.data_time_format))
        self.assertEqual(resp_data['values'][0], 4)
        self.assertEqual(resp_data['values'][1], 3)
        self.assertEqual(resp_data['metric_type'], data['metric_type'])

        data['server'] = 'test1'
        response = self.client.post(url, data=json.dumps(data), follow_redirects=True, content_type='application/json')
        resp_data = json.loads(response.data.decode('utf-8'))['data']
        self.assertEqual(len(resp_data['timeline']), 2)
        self.assertEqual(resp_data['timeline'][0], self.time1.strftime(self.data_time_format))
        self.assertEqual(resp_data['timeline'][1], self.time2.strftime(self.data_time_format))
        self.assertEqual(resp_data['values'][0], 2)
        self.assertEqual(resp_data['values'][1], 2)
        self.assertEqual(resp_data['metric_type'], data['metric_type'])

        data['step'] = self.week * 4
        response = self.client.post(url, data=json.dumps(data), follow_redirects=True, content_type='application/json')
        resp_data = json.loads(response.data.decode('utf-8'))['data']
        self.assertEqual(len(resp_data['timeline']), 1)
        self.assertEqual(resp_data['timeline'][0], self.time1.strftime(self.data_time_format))
        self.assertEqual(resp_data['metric_type'], data['metric_type'])

    @staticmethod
    def request_without_ruquied_field(client, url, data, field):
        value = data[field]
        data.pop(field)
        response = client.post(url, data=json.dumps(data), follow_redirects=True, content_type='application/json')
        data[field] = value
        return response
