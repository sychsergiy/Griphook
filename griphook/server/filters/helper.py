from griphook.server.models import Service, ServicesGroup, Server, Cluster

from sqlalchemy.sql.functions import array_agg


def get_clusters_hierarchy_part():
    clusters_query = Cluster.query.with_entities(Cluster.id, Cluster.title)
    clusters = tuple(
        {"id": id_, "title": title} for (id_, title) in clusters_query
    )
    return clusters


def get_servers_hierarchy_part():
    servers_query = Server.query.with_entities(
        Server.id, Server.title, Server.cluster_id
    )

    servers = tuple(
        {"id": id_, "title": server, "cluster_id": cluster_id}
        for (id_, server, cluster_id) in servers_query
    )
    return servers


def get_services_groups_hierarchy_part():
    services_groups_query = (
        ServicesGroup.query.join(Service)
        .join(Server)
        .group_by(ServicesGroup.title, ServicesGroup.id)
        .with_entities(
            ServicesGroup.id,
            ServicesGroup.title,
            array_agg(Service.server_id).label("servers_ids"),
            array_agg(Server.cluster_id).label("clusters_ids"),
        )
    )

    services_groups = tuple(
        {
            "id": id_,
            "title": title,
            "servers_ids": list(set(servers_ids)),
            "clusters_ids": list(set(clusters_ids)),
        }
        for (id_, title, servers_ids, clusters_ids) in services_groups_query
    )
    return services_groups


def get_services_hierarchy_part():
    services_query = (
        Service.query.join(ServicesGroup)
        .join(Server)
        .distinct()
        .with_entities(
            Service.id,
            Service.title,
            Service.instance,
            Service.server_id,
            Service.services_group_id,
            Server.cluster_id,
        )
    )
    # todo: Is it really necessary to use distinct?

    services = tuple(
        {
            "id": id_,
            "title": service,
            "instance": instance,
            "server_id": server_id,
            "group_id": group_id,
            "cluster_id": cluster_id,
        }
        for (
            id_,
            service,
            instance,
            server_id,
            group_id,
            cluster_id,
        ) in services_query
    )
    return services
