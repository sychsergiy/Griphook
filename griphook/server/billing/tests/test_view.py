from flask import url_for

from griphook.tests.base import BaseTestCase


class BillingTableViewTestCase(BaseTestCase):

    def test_view_return_405_status_if_empty_json_given(self):
        response = self.client.post(url_for('billing.billing-table',
                                            data={}))

        self.assert405(response)

    def test_view_return_400_status_if_time_not_specified(self):
        # No time_since and time_until given
        response = self.client.post(url_for('billing.billing-table',
                                            data={
                                                "services_groups": "adv-stable",
                                                "team": "prom",
                                                "project": "shafa",
                                                "cluster": "olympus",
                                                "server": "adv"
                                                }))
        self.assert400(response)

        # No time_until given
        response = self.client.post(url_for('billing.billing-table',
                                            data={"time_from": "2018-05-01"}))
        self.assert400(response)
        # No time_since given
        response = self.client.post(url_for('billing.billing-table',
                                            data={"time_until": "2018-05-01"}))
        self.assert400(response)
