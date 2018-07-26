from flask import jsonify, request, abort

from griphook.server.models import Service, ServicesGroup


def servers_api_view():
    servers_field_set = (
        Service.query.with_entities(Service.server)
            .distinct().order_by('server').all()
    )
    response = jsonify([field_set[0] for field_set in servers_field_set])
    response.status_code = 200
    return response


def services_groups_api_view():
    server_title = request.args.get('server_title')
    if not server_title:
        abort(400)

    services_groups_field_set = (
        Service.query
            .filter(Service.server == server_title)
            .distinct().join(ServicesGroup)
            .with_entities(ServicesGroup.title)
            .order_by(ServicesGroup.title)
    ).all()

    response = jsonify([field_set[0] for field_set in services_groups_field_set])
    response.status_code = 200
    return response


def services_api_view():
    services_group_title = request.args.get('services_group_title')
    if not services_group_title:
        abort(400)

    service_field_set = (
        Service.query
            .with_entities(Service.title).join(ServicesGroup)
            .filter(ServicesGroup.title == services_group_title)
    ).all()

    response = jsonify([field_set[0] for field_set in service_field_set])
    response.status_code = 200
    return response
