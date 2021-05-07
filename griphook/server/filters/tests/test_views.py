import pytest

from flask import url_for


@pytest.fixture
def services_hierarchy_part():
    services = [
        {
            "cluster_id": 2,
            "group_id": 1,
            "id": 4,
            "instance": "0",
            "server_id": 3,
            "title": "service4",
        }
    ]
    return services


@pytest.fixture
def servers_hierarchy_part():
    servers = [{"cluster_id": 2, "id": 3, "title": "Server3"}]
    return servers


@pytest.fixture
def clusters_hierarchy_part():
    clusters = [
        {
            "cluster_id": 2,
            "group_id": 1,
            "id": 4,
            "instance": "0",
            "server_id": 3,
            "title": "service4",
        }
    ]
    return clusters


@pytest.fixture
def groups_hierarchy_part():
    groups = [
        {
            "clusters_ids": [1, 2],
            "id": 1,
            "servers_ids": [1, 2, 3],
            "title": "group1",
        }
    ]
    return groups


@pytest.fixture
def teams_hierarchy_part():
    teams = [{"id": 1, "title": "team1"}, {"id": 2, "title": "team2"}]
    return teams


@pytest.fixture
def projects_hierarchy_part():
    projects = [{"id": 1, "title": "team1"}, {"id": 2, "title": "team2"}]
    return projects


@pytest.mark.usefixtures("client_class")
class TestGetPeaksFiltersHierarchyView(object):
    def test_view_return_correct_response(
        self,
        mocker,
        services_hierarchy_part,
        servers_hierarchy_part,
        clusters_hierarchy_part,
        groups_hierarchy_part,
    ):
        mocker.patch(
            "griphook.server.filters.views.get_services_hierarchy_part",
            return_value=services_hierarchy_part,
        )
        mocker.patch(
            "griphook.server.filters.views.get_servers_hierarchy_part",
            return_value=servers_hierarchy_part,
        )
        mocker.patch(
            "griphook.server.filters.views.get_services_groups_hierarchy_part",
            return_value=groups_hierarchy_part,
        )
        mocker.patch(
            "griphook.server.filters.views.get_clusters_hierarchy_part",
            return_value=clusters_hierarchy_part,
        )

        expected_response = {
            "services": services_hierarchy_part,
            "clusters": clusters_hierarchy_part,
            "services_groups": groups_hierarchy_part,
            "servers": servers_hierarchy_part,
        }

        response = self.client.get(url_for("filters.peaks"))
        assert response.status_code == 200
        assert response.json == expected_response

    def test_405_status_code_on_post(self):
        response = self.client.post(url_for("filters.peaks"))
        assert response.status_code == 405


@pytest.mark.usefixtures("client_class")
class TestGetBillingFiltersHierarchyView(object):
    def test_view_return_correct_response(
        self,
        mocker,
        services_hierarchy_part,
        servers_hierarchy_part,
        clusters_hierarchy_part,
        groups_hierarchy_part,
        projects_hierarchy_part,
        teams_hierarchy_part,
    ):
        mocker.patch(
            "griphook.server.filters.views.get_services_hierarchy_part",
            return_value=services_hierarchy_part,
        )
        mocker.patch(
            "griphook.server.filters.views.get_servers_hierarchy_part",
            return_value=servers_hierarchy_part,
        )
        mocker.patch(
            "griphook.server.filters.views.get_services_groups_hierarchy_part",
            return_value=groups_hierarchy_part,
        )
        mocker.patch(
            "griphook.server.filters.views.get_clusters_hierarchy_part",
            return_value=clusters_hierarchy_part,
        )

        mocker.patch(
            "griphook.server.filters.views.get_teams_hierarchy_part",
            return_value=teams_hierarchy_part,
        )

        mocker.patch(
            "griphook.server.filters.views.get_projects_hierarchy_part",
            return_value=projects_hierarchy_part,
        )

        expected_response = {
            "services": services_hierarchy_part,
            "clusters": clusters_hierarchy_part,
            "services_groups": groups_hierarchy_part,
            "servers": servers_hierarchy_part,
            "teams": teams_hierarchy_part,
            "projects": projects_hierarchy_part,
        }

        response = self.client.get(url_for("filters.billing"))
        assert response.status_code == 200
        assert response.json == expected_response

    def test_405_status_code_on_post(self):
        response = self.client.post(url_for("filters.billing"))
        assert response.status_code == 405
