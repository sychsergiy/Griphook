from griphook.server.filters.billing_queries import (
    get_projects_hierarchy_part,
    get_teams_hierarchy_part,
)


def test_get_all_projects_converted_to_dict(projects):
    real_projects = get_projects_hierarchy_part()
    expected_projects = tuple(
        [
            {"id": 1, "title": "project1", "services_group_ids": [1]},
            {"id": 2, "title": "project2", "services_group_ids": []},
            {"id": 3, "title": "project3", "services_group_ids": []},
        ]
    )
    assert real_projects == expected_projects


def test_get_all_teams_converted_to_dict(teams):
    real_teams = get_teams_hierarchy_part()
    expected_projects = tuple(
        [
            {"id": 1, "title": "team1", "services_group_ids": [1]},
            {"id": 2, "title": "team2", "services_group_ids": []},
            {"id": 3, "title": "team3", "services_group_ids": []},
        ]
    )
    assert real_teams == expected_projects
