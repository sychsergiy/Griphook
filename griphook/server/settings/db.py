from griphook.server.models import Project, Team, Server, Cluster, ServicesGroup, Service


class DataBase:
    @staticmethod
    def get_projects(session):
        projects_query = session.query(Project.id, Project.title).all()
        return projects_query

    @staticmethod
    def get_teams(session):
        teams_query = session.query(Team.id, Team.title).all()
        return teams_query

    @staticmethod
    def get_servers(session):
        servers_query = session.query(Server.id, Server.title).all()
        return servers_query

    @staticmethod
    def get_clusters(session):
        clusters_query = session.query(Cluster.id, Cluster.title).all()
        return clusters_query

    @staticmethod
    def get_services_group(session):
        services_groups_query = session.query(ServicesGroup.id, ServicesGroup.title, ServicesGroup.project_id, ServicesGroup.team_id).all()
        return services_groups_query

    @staticmethod
    def get_services_for_services_group(session, services_group_id):
        services_query = session.query(Service.id, Service.title).filter_by(services_group_id=services_group_id).all()
        return services_query
