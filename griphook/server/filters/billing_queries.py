from griphook.server.models import Team, Project


def get_teams_hierarchy_part():
    teams_query = Team.query.with_entities(Team.id, Team.title).all()
    teams = tuple(
        {"id": id_, "title": title, } for (id_, title) in teams_query
    )
    return teams


def get_projects_hierarchy_part():
    projects_query = Project.query.with_entities(Project.id, Project.title).all()

    projects = tuple(
        {"id": id_, "title": title} for (id_, title) in projects_query
    )
    return projects
