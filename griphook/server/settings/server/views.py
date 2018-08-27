import json

from flask import request, jsonify
from flask.views import View
from pydantic import ValidationError

from griphook.server import db
from griphook.server.settings.db import DataBase
from griphook.server.managers.server_manager import ServerManager
from griphook.server.settings.validators import UpdateServerClusterModel
from griphook.server.managers.exceptions import ServerManagerException
from griphook.server.settings.constants import (
    EXC_FIELD_IS_REQUIRED,
    PARAMETERS_SERVER_CLUSTER_CPU_PRICE,
    PARAMETERS_SERVER_CLUSTER_MEMORY_PRICE,
)


class GetServers(View):
    """
    API method for getting all servers.
    """

    methods = ["GET"]

    def dispatch_request(self):
        servers_query = DataBase.get_servers(db.session)
        servers = [
            {"id": server_id, "title": server_title}
            for (server_id, server_title) in servers_query
        ]
        return jsonify({"servers": servers})


class ServerUpdateCPUPrice(View):
    """
    API method for update server CPU price.

    Incoming data format:
    {
        "id": integer | required,
        "cpu_price": float | required
    }

    If the incoming data is not valid or server doesn't exists,
    the error information will be returned.

    Result data format:
    {
        "success": boolean
    }
    """

    methods = ["PUT"]

    def dispatch_request(self):
        data_for_update = json.loads(request.data)

        for parameter in PARAMETERS_SERVER_CLUSTER_CPU_PRICE:
            if parameter not in data_for_update:
                return (
                    jsonify({"error": EXC_FIELD_IS_REQUIRED.format(parameter)}),
                    400,
                )
        try:
            valid_data_for_create = UpdateServerClusterModel(**data_for_update)
        except ValidationError as e:
            return jsonify({"error": e.errors()}), 400
        try:
            ServerManager(db.session).set_cpu_price(
                server_id=valid_data_for_create.id,
                new_cpu_price=valid_data_for_create.cpu_price,
            )
        except ServerManagerException as exc:
            return jsonify({"error": exc.error_text}), 400
        return jsonify({"success": True})


class ServerUpdateMemoryPrice(View):
    """
    API method for update server memory price.

    Incoming data format:
    {
        "id": integer | required,
        "memory_price": float | required
    }

    If the incoming data is not valid or server doesn't exists,
    the error information will be returned.

    Result data format:
    {
        "success": boolean
    }
    """

    methods = ["PUT"]

    def dispatch_request(self):
        data_for_update = json.loads(request.data)

        for parameter in PARAMETERS_SERVER_CLUSTER_MEMORY_PRICE:
            if parameter not in data_for_update:
                return (
                    jsonify({"error": EXC_FIELD_IS_REQUIRED.format(parameter)}),
                    400,
                )
        try:
            valid_data_for_create = UpdateServerClusterModel(**data_for_update)
        except ValidationError as e:
            return jsonify({"error": e.errors()}), 400
        try:
            ServerManager(db.session).set_memory_price(
                server_id=valid_data_for_create.id,
                new_memory_price=valid_data_for_create.memory_price,
            )
        except ServerManagerException as exc:
            return jsonify({"error": exc.error_text}), 400
        return jsonify({"success": True})
