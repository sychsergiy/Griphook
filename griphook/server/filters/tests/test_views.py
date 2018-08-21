import pytest

from flask import url_for


@pytest.mark.usefixtures("client_class")
class TestGetPeaksFiltersHierarchyView(object):
    def test_view_return_correct_response(self, mocker):
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
        servers = [{"cluster_id": 2, "id": 3, "title": "Server3"}]
        services_groups = [
            {
                "clusters_ids": [1, 2],
                "id": 1,
                "servers_ids": [1, 2, 3],
                "title": "group1",
            }
        ]
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

        mocker.patch(
            "griphook.server.filters.views.get_services_hierarchy_part",
            return_value=services,
        )
        mocker.patch(
            "griphook.server.filters.views.get_servers_hierarchy_part",
            return_value=servers,
        )
        mocker.patch(
            "griphook.server.filters.views.get_services_groups_hierarchy_part",
            return_value=services_groups,
        )
        mocker.patch(
            "griphook.server.filters.views.get_clusters_hierarchy_part",
            return_value=clusters,
        )

        expected_response = {
            "services": services,
            "clusters": clusters,
            "services_groups": services_groups,
            "servers": servers,
        }

        response = self.client.get(url_for("filters.peaks"))
        assert response.status_code == 200
        assert response.json == expected_response

    def test_405_status_code_on_post(self):
        response = self.client.post(url_for("filters.peaks"))
        assert response.status_code == 405
