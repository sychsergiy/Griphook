# from griphook.tests.base import BaseTestCase
#
# from griphook.server.average_load.helper import (
#     ServerChartDataHelper,
#     ServicesGroupChartDataHelper,
#     ServicesChartDataHelper)
# from griphook.server.average_load.graphite import construct_target, summarize, average
# from griphook.server.models import Service, ServicesGroup
# from griphook.server import db
#
#
# class ServerChartDataHelperTestCase(BaseTestCase):
#     def setUp(self):
#         super(ServerChartDataHelperTestCase, self).setUp()
#         self.server = 'server1'
#         self.metric_type = 'vsize'
#
#         sv_group1 = ServicesGroup(title='service_group1')  # in query
#         sv_group2 = ServicesGroup(title='service_group2')  # not in query
#         sv_group3 = ServicesGroup(title='service_group3')  # not in query
#         sv_group4 = ServicesGroup(title='service_group4')  # in query
#
#         db.session.add_all([sv_group1, sv_group2, sv_group3])
#
#         db.session.add_all([
#             Service(title='service1', services_group=sv_group1, server='server1', instance=0),  #
#             Service(title='service2', services_group=sv_group1, server='server2', instance=0),  # sv_group1 in few servers
#             Service(title='service3', services_group=sv_group2, server='server2', instance=0),  # not in query
#             Service(title='service4', services_group=sv_group1, server='server1', instance=0),  # ignored by distinct statement
#             Service(title='service5', services_group=sv_group4, server='server1', instance=0),  # simple sv_group4 in server1
#         ])
#         db.session.commit()
#         self.server_helper = ServerChartDataHelper(self.server, self.metric_type)
#
#     def test_retrieve_children_method(self):
#         children = self.server_helper.retrieve_children()
#         expected_children = ('service_group1', 'service_group4')
#         self.assertEqual(children, expected_children)
#
#     def test_parent_target_constructor_method(self):
#         target = self.server_helper.root_target_constructor()
#         expected_target = construct_target(self.metric_type, self.server)
#
#         self.assertEqual(target, expected_target)
#
#     def test_parent_target_method(self):
#         target = self.server_helper.root_target()
#         expected_target = average(summarize(construct_target(self.metric_type, self.server)))
#
#         self.assertEqual(target, expected_target)
#
#     def test_children_target_constructor(self):
#         target = self.server_helper.children_target_constructor('service_group1')
#         expected_target = construct_target(self.metric_type, server=self.server, services_group='service_group1')
#
#         self.assertEqual(target, expected_target)
#
#     def test_children_target(self):
#         target = list(self.server_helper.children_target())
#
#         expected_target = [
#             average(summarize(self.server_helper.children_target_constructor('service_group1'))),
#             average(summarize(self.server_helper.children_target_constructor('service_group4'))),
#         ]
#
#         self.assertEqual(target, expected_target)
#
#     # todo test get_data method
#
#
# class ServicesGroupChartDataHelperTestCase(BaseTestCase):
#     def setUp(self):
#         super(ServicesGroupChartDataHelperTestCase, self).setUp()
#         self.service_group = 'service_group1'
#         self.metric_type = 'vsize'
#
#         sv_group1 = ServicesGroup(title='service_group1')
#         sv_group2 = ServicesGroup(title='service_group2')
#
#         db.session.add_all([sv_group1, sv_group2])
#         db.session.add_all([
#             Service(title='service1', services_group=sv_group1, instance=0),  # in query
#             Service(title='service2', services_group=sv_group1, instance=0),  # in query
#             Service(title='service3', services_group=sv_group2, instance=0),  # not in query
#         ])
#         db.session.commit()
#         self.sv_group_helper = ServicesGroupChartDataHelper(self.service_group, self.metric_type)
#
#     def test_retrieve_children_method(self):
#         children = self.sv_group_helper.retrieve_children()
#
#         expected_children = ('service1', 'service2')
#         self.assertEqual(children, expected_children)
#
#     def test_parent_target_constructor_method(self):
#         target = self.sv_group_helper.root_target_constructor()
#         expected_target = construct_target(self.metric_type, services_group=self.service_group)
#         self.assertEqual(target, expected_target)
#
#     def test_parent_target_method(self):
#         target = self.sv_group_helper.root_target()
#         expected_target = average(summarize(construct_target(self.metric_type, services_group=self.service_group)))
#         self.assertEqual(target, expected_target)
#
#     def test_children_target_constructor(self):
#         target = self.sv_group_helper.children_target_constructor('service1')
#         expected_target = construct_target(self.metric_type, services_group=self.service_group, service='service1')
#
#         self.assertEqual(target, expected_target)
#
#     def test_children_target(self):
#         target = list(self.sv_group_helper.children_target())
#
#         expected_target = [
#             average(summarize(self.sv_group_helper.children_target_constructor('service1'))),
#             average(summarize(self.sv_group_helper.children_target_constructor('service2'))),
#         ]
#
#         self.assertEqual(target, expected_target)
#
#
# class ServicesChartDataHelperTestCase(BaseTestCase):
#     def setUp(self):
#         super(ServicesChartDataHelperTestCase, self).setUp()
#         self.service = 'service1'
#         self.metric_type = 'vsize'
#
#         sv_group1 = ServicesGroup(title='services_group1')
#         sv_group2 = ServicesGroup(title='services_group2')
#
#         services = [
#             Service(title=self.service, instance=0, services_group=sv_group1),  # in query
#             Service(title=self.service, instance=0, services_group=sv_group2),  # in query, because sv_group different
#             Service(title=self.service, instance=1, services_group=sv_group1),  # in query
#
#             Service(title='service2', instance=1, services_group=sv_group1),  # no in query
#         ]
#
#         db.session.add_all([sv_group1, sv_group2])
#         db.session.add_all(services)
#         db.session.commit()
#
#         self.services_helper = ServicesChartDataHelper(self.service, self.metric_type)
#
#         self.children_item = ('services_group1', self.service, '0')
#
#     def test_retrieve_children_method(self):
#         children = self.services_helper.retrieve_children()
#
#         expected_children = [
#             ('services_group1', self.service, '0'),
#             ('services_group1', self.service, '1'),
#             ('services_group2', self.service, '0'),
#         ]
#         self.assertEqual(children, expected_children)
#
#     def test_parent_target_constructor_method(self):
#         target = self.services_helper.root_target_constructor()
#         expected_target = construct_target(self.metric_type, service=self.service)
#         self.assertEqual(target, expected_target)
#
#     def test_parent_target_method(self):
#         target = self.services_helper.root_target()
#         expected_target = average(summarize(construct_target(self.metric_type, service=self.service)))
#         self.assertEqual(target, expected_target)
#
#     def test_children_target_constructor(self):
#         target = self.services_helper.children_target_constructor(self.children_item)
#         expected_target = construct_target(self.metric_type, '*', *self.children_item)
#
#         self.assertEqual(target, expected_target)
#
#     def test_children_target(self):
#         target = list(self.services_helper.children_target())
#         expected_target = [
#             average(
#                 summarize(self.services_helper.children_target_constructor(('services_group1', self.service, '0')))),
#             average(
#                 summarize(self.services_helper.children_target_constructor(('services_group1', self.service, '1')))),
#             average(
#                 summarize(self.services_helper.children_target_constructor(('services_group2', self.service, '0')))),
#         ]
#         self.assertEqual(target, expected_target)
