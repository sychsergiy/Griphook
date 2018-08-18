from flask import jsonify

from griphook.server.filters.peaks_queries import (
    get_clusters_hierarchy_part,
    get_servers_hierarchy_part,
    get_services_groups_hierarchy_part,
    get_services_hierarchy_part,
)

from griphook.server.filters.billing_queries import (
    get_all_teams_converted_to_dict,
    get_all_projects_converted_to_dict
)


def get_peaks_filters_hierarchy():
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
    """
    clusters = get_clusters_hierarchy_part()
    servers = get_servers_hierarchy_part()
    services_groups = get_services_groups_hierarchy_part()
    services = get_services_hierarchy_part()

    response_data = {
        "clusters": clusters,
        "servers": servers,
        "services_groups": services_groups,
        "services": services,
    }
    return jsonify(response_data)


def get_billing_filters_hierarchy():
    """
    Endpoint to get full hierarchy of ...
    in following format:
    {
      "teams    ": [
        {
          "id": "id",
          "title": "title"
        }
      ],
      "projects": [
        {
          "id": "id",
          "title": "title"
        }
      ],
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
    """
    teams = get_all_teams_converted_to_dict()
    projects = get_all_projects_converted_to_dict()

    clusters = get_clusters_hierarchy_part()
    servers = get_servers_hierarchy_part()
    services_groups = get_services_groups_hierarchy_part()
    services = get_services_hierarchy_part()

    response_data = {
        "teams": teams,
        "projects": projects,

        "clusters": clusters,
        "servers": servers,
        "services_groups": services_groups,
        "services": services,

    }
    return jsonify(response_data)
