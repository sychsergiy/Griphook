from flask import request, jsonify
from flask.views import View

from sqlalchemy import func

from griphook.server.models import (
    ServicesGroup,
    Service,
    MetricBilling,
    BatchStoryBilling,
    Cluster,
    Server,
    Team,
    Project,
)


class GetPieChartAbsoluteDataView(View):
    """
    request format:
      {
        "target_type": one_of(project, team, cluster, server, services_group, all),
        "target_ids": [int],
        "time_from": "Y-M-D"
        "metric_type": one_of("user_cpu_percent", "vsize")
        "time_until": "Y-M-D"
      }
      response format:
      {
        "labels": [str],
        "values": [int],
      ]

    """

    methods = ["POST"]

    def dispatch_request(self):
        # todo: input data validation
        request_data = request.get_json()
        # todo: check if target_ids are in db, else abort 404
        total_initial_query = ServicesGroup.query
        total_metric_sum = self.get_query_metric_sum(total_initial_query, request_data)

        target_type = request_data["target_type"]
        target_ids = request_data["target_ids"]
        # todo: change on hash map
        if target_type == "all":
            initial_query = total_initial_query
        elif target_type == "cluster":
            initial_query = (
                Cluster.query.filter(Cluster.id.in_(target_ids))
                    .join(Server)
                    .join(Service)
            )
        elif target_type == "server":
            initial_query = Server.query.filter(Server.id.in_(target_ids)).join(Service)
        elif target_type == "services_group":
            initial_query = ServicesGroup.query.filter(ServicesGroup.id.in_(target_ids))
        elif target_type == "team":
            initial_query = Team.query
        elif target_type == "project":
            initial_query = Project.query
        else:
            raise Exception("Problem with request data validation")

        selected_metric_sum = self.get_query_metric_sum(
            initial_query, request_data
        )
        # if target ids are not found and selected_metric_sum is None, just set 0
        # todo: maybe it will be better to return 404
        selected_metric_sum = selected_metric_sum if selected_metric_sum else 0

        response_data = {
            "labels": ["selected", "rest"],
            "values": [
                # todo: solve problem with ceiling in big number
                selected_metric_sum,
                total_metric_sum - selected_metric_sum,
            ],
        }
        return jsonify(response_data)

    def get_query_metric_sum(self, initial_query, request_data):
        """
        :param initial_query: query before joining with
         MetricBillling table, must be joined with Service or ServicesGroup
        """
        metric_sum = (
            initial_query.join(MetricBilling)
                .join(BatchStoryBilling)
                .filter(MetricBilling.type == request_data["metric_type"])
                .filter(
                BatchStoryBilling.time.between(
                    request_data["time_from"], request_data["time_until"]
                )
            )
                .with_entities(func.sum(MetricBilling.value).label("metric_sum"))
        ).scalar()
        return metric_sum


class GetPieChartRelativeDataView(View):
    """
    request format:
      {
        "target_type": one_of(project, team, cluster, server, services_group, all),
        "target_ids": [int],
        "time_from": "Y-M-D"
        "metric_type": one_of("user_cpu_percent", "vsize")
        "time_until": "Y-M-D"
      }
      response format:
      {
        "labels": [str],
        "values": [int],
      ]

    """

    methods = ["POST"]

    def dispatch_request(self):
        request_data = request.get_json()

        total = (
            ServicesGroup.query.join(Service)
                .join(MetricBilling)
                .join(BatchStoryBilling)
                .filter(MetricBilling.type == request_data["metric_type"])
                .filter(
                BatchStoryBilling.time.between(
                    request_data["time_from"], request_data["time_until"]
                )
            )
                .group_by(ServicesGroup.title)
                .order_by(func.sum(MetricBilling.value).desc())
                .with_entities(
                ServicesGroup.title, func.sum(MetricBilling.value).label("metric_sum")
            )
        )

        print(total)

        # if request_data['target_type'] == 'all':
        #     passResource
