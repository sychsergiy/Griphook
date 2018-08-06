from griphook.server.models import Service, ServicesGroup


def get_clusters_with_ids():
    clusters_query = (
        Service.query
            .distinct()
            .with_entities(Service.cluster)
    )
    clusters = tuple({'id': title, "title": title} for (title,) in clusters_query)
    # todo: use cluster title as id until models updating
    return clusters


def get_servers_with_ids():
    servers_query = (
        Service.query
            .distinct()
            .with_entities(Service.server, Service.cluster)
    )

    servers = tuple(
        {'id': server, 'title': server, 'cluster_id': cluster}
        for (server, cluster) in servers_query
    )
    # todo: use server title as id until models updating
    return servers


def get_services_groups_with_ids():
    services_groups_query = (
        ServicesGroup.query
            .with_entities(ServicesGroup.id, ServicesGroup.title)
    )

    services_groups = tuple(
        {"id": id_, "title": title} for (id_, title) in services_groups_query
    )
    return services_groups


def get_services_with_ids():
    services_query = (
        Service.query
            .join(ServicesGroup).distinct()
            .with_entities(Service.id, Service.title, Service.instance, Service.server,
                           ServicesGroup.id, Service.cluster, )
    )
    # todo: Is it really necessary to use distinct?

    services = tuple(
        {"id": id_, 'title': service, 'instance': instance,
         'server_id': server_id, 'group_id': group_id, 'cluster_id': cluster_id}
        for (id_, service, instance, server_id, group_id, cluster_id) in services_query
    )
    # todo: use server and cluster titles as id server_id and cluster_id until models updating
    return services