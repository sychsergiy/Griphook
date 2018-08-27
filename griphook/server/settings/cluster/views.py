import json

from flask import request, jsonify
from flask.views import View
from pydantic import ValidationError

from griphook.server import db
from griphook.server.settings.db import DataBase
from griphook.server.managers.cluster_manager import ClusterManager
from griphook.server.settings.validators import UpdateServerClusterModel
from griphook.server.managers.exceptions import ClusterManagerException
from griphook.server.settings.constants import (
    EXC_FIELD_IS_REQUIRED,
    PARAMETERS_SERVER_CLUSTER_CPU_PRICE,
    PARAMETERS_SERVER_CLUSTER_MEMORY_PRICE
)


class GetClusters(View):
    methods = ['GET']

    def dispatch_request(self):
        clusters_query = DataBase.get_clusters(db.session)
        clusters = [{"id": cluster_id, "title": cluster_title} for (cluster_id, cluster_title) in clusters_query]
        return jsonify(
            {'clusters': clusters}
        )


class ClusterUpdateCPUPrice(View):
    methods = ['PUT']

    def dispatch_request(self):
        data_for_update = json.loads(request.data)

        for parameter in PARAMETERS_SERVER_CLUSTER_CPU_PRICE:
            if parameter not in data_for_update:
                return jsonify(
                    {'error': EXC_FIELD_IS_REQUIRED.format(parameter)}
                ), 400
        try:
            valid_data_for_create = UpdateServerClusterModel(**data_for_update)
        except ValidationError as e:
            return jsonify(
                {'error': e.errors()}
            ), 400
        try:
            ClusterManager(db.session).set_cpu_price(
                cluster_id=valid_data_for_create.id,
                new_cpu_price=valid_data_for_create.cpu_price
            )
        except ClusterManagerException as exc:
            return jsonify(
                {'error': exc.error_text}
            ), 400
        return jsonify(
            {'success': True}
        )


class ClusterUpdateMemoryPrice(View):
    methods = ['PUT']

    def dispatch_request(self):
        data_for_update = json.loads(request.data)

        for parameter in PARAMETERS_SERVER_CLUSTER_MEMORY_PRICE:
            if parameter not in data_for_update:
                return jsonify(
                    {'error': EXC_FIELD_IS_REQUIRED.format(parameter)}
                ), 400
        try:
            valid_data_for_create = UpdateServerClusterModel(**data_for_update)
        except ValidationError as e:
            return jsonify(
                {'error': e.errors()}
            ), 400
        try:
            ClusterManager(db.session).set_memory_price(
                cluster_id=valid_data_for_create.id,
                new_memory_price=valid_data_for_create.memory_price
            )
        except ClusterManagerException as exc:
            return jsonify(
                {'error': exc.error_text}
            ), 400
        return jsonify(
            {'success': True}
        )
