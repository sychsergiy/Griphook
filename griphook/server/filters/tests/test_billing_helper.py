from griphook.server.filters.billing_queries import (
    get_projects_hierarchy_part,
    get_teams_hierarchy_part,
)


def test_get_all_projects_converted_to_dict(projects):
    real_projects = get_projects_hierarchy_part()
    expected_projects = tuple({"id": id_, "title": title} for (id_, title) in projects)
    assert real_projects == expected_projects


def test_get_all_teams_converted_to_dict(teams):
    real_teams = get_teams_hierarchy_part()
    expected_projects = tuple({"id": id_, "title": title} for (id_, title) in teams)
    assert real_teams == expected_projects
