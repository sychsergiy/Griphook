from sqlalchemy.sql.functions import array_agg

from griphook.server.models import Team, Project, ServicesGroup


def get_teams_hierarchy_part():
    teams_query = (
        Team.query.outerjoin(ServicesGroup, ServicesGroup.team_id == Team.id)
        .group_by(Team.id, Team.title)
        .with_entities(
            Team.id,
            Team.title,
            array_agg(ServicesGroup.id).label("services_group_ids"),
        )
    ).all()

    teams = tuple(
        {
            "id": id_,
            "title": title,
            "services_group_ids": list(
                set(group_id for group_id in group_ids if group_id is not None)
            ),
        }
        for (id_, title, group_ids) in teams_query
    )
    # todo: separate None ids skipping or dot it using sqlalchemy
    # todo: add one more test on group_ids=[None] case
    return teams


def get_projects_hierarchy_part():
    projects_query = (
        Project.query.outerjoin(
            ServicesGroup, Project.id == ServicesGroup.project_id
        )
        .group_by(Project.id, Project.title)
        .with_entities(
            Project.id,
            Project.title,
            array_agg(ServicesGroup.id).label("services_group_ids"),
        )
    ).all()

    projects = tuple(
        {
            "id": id_,
            "title": title,
            "services_group_ids": list(
                set(group_id for group_id in group_ids if group_id is not None)
            ),
        }
        for (id_, title, group_ids) in projects_query
    )
    # todo: separate None ids skipping or dot it using sqlalchemy
    # todo: add one more test on group_ids=[None] case
    return projects
