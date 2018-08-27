from operator import itemgetter

from griphook.server.filters.peaks_queries import (
    get_services_groups_hierarchy_part,
    get_clusters_hierarchy_part,
    get_servers_hierarchy_part,
    get_services_hierarchy_part,
)


def test_get_clusters_hierarchy_part(clusters):
    real_clusters = get_clusters_hierarchy_part()

    expected_clusters = tuple({"id": id_, "title": title} for (id_, title) in clusters)

    assert real_clusters == expected_clusters


def test_get_servers_hierarchy_part(servers):
    real_servers = get_servers_hierarchy_part()

    expected_servers = tuple(
        {"id": id_, "title": title, "cluster_id": cluster_id}
        for (id_, title, cluster_id) in servers
    )
    assert real_servers == expected_servers


def test_get_services_groups_hierarchy_part(services_groups_with_servers_and_clusters):
    services_groups = get_services_groups_hierarchy_part()
    expected_services_groups = (
        {"id": 1, "title": "group1", "servers_ids": [1, 2, 3], "clusters_ids": [1, 2]},
        {"id": 2, "title": "group2", "servers_ids": [3], "clusters_ids": [2]},
    )
    assert services_groups == expected_services_groups


def test_get_services_hierarchy_part(services_groups_with_servers_and_clusters):
    services = tuple(sorted(get_services_hierarchy_part(), key=itemgetter("id")))
    expected_services = (
        {
            "id": 1,
            "title": "service1",
            "instance": "0",
            "server_id": 1,
            "group_id": 1,
            "cluster_id": 1,
        },
        {
            "id": 2,
            "title": "service2",
            "instance": "0",
            "server_id": 1,
            "group_id": 1,
            "cluster_id": 1,
        },
        {
            "id": 3,
            "title": "service3",
            "instance": "0",
            "server_id": 2,
            "group_id": 1,
            "cluster_id": 1,
        },
        {
            "id": 4,
            "title": "service4",
            "instance": "0",
            "server_id": 3,
            "group_id": 1,
            "cluster_id": 2,
        },
        {
            "id": 5,
            "title": "service5",
            "instance": "0",
            "server_id": 3,
            "group_id": 2,
            "cluster_id": 2,
        },
    )
    assert expected_services == services
