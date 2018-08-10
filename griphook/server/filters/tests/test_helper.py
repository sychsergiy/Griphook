from griphook.server.filters.helper import get_clusters_hierarchy_part, get_servers_hierarchy_part


def test_get_clusters_hierarchy_part(clusters):
    real_clusters = get_clusters_hierarchy_part()

    expected_clusters = tuple(
        {"id": id_, "title": title} for (id_, title) in clusters
    )

    assert real_clusters == expected_clusters


def test_get_servers_hierarchy_part(servers):
    real_servers = get_servers_hierarchy_part()

    expected_servers = tuple(
        {"id": id_, "title": title, "cluster_id": cluster_id} for (id_, title, cluster_id) in servers
    )
    assert real_servers == expected_servers
