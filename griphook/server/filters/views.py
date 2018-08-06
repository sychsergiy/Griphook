from flask import jsonify

from griphook.server.filters.helper import (
    get_clusters_with_ids,
    get_servers_with_ids,
    get_services_groups_with_ids,
    get_services_with_ids
)


def filters_hierarchy_api_view():
    """
    Endpoint to get full hierarchy of ...
    in following format:
    {
      "clusters": [
        {
          "id": "id",
          "title": "title"
        }
      ],
      "servers": [
        {
          "id": "id",
          "title": "title",
          "cluster_id": "cluster_id"
        }
      ],
      "services_groups": [
        {
          "id": "id",
          "title": "title",
          "server_ids": [],
          "clusters_ids": []
        }
      ]

      "services": [
        {
          "id": "id",
          "title": "title",
          "group": "services_group_id",
          "server_id": "server_id",
          "cluster_id": "cluster_id"
        }
      ]
    }
    :return:
    """
    clusters = get_clusters_with_ids()
    servers = get_servers_with_ids()
    services_groups = get_services_groups_with_ids()
    services = get_services_with_ids()

    response_data = {
        'clusters': clusters,
        'servers': servers,
        'services_groups': services_groups,
        'services': services,
    }
    return jsonify(response_data)
