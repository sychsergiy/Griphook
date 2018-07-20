import unittest

from griphook.cli.managers.base import Manager, ManagerException
from griphook.db.models import Team, Project, ServicesGroup

from griphook.cli.tests.base import BaseWithDBSession


class ManagerTestCase(BaseWithDBSession):
    def setUp(self):
        self.manager = Manager(self.session)
        self.clean_up_db()

    def test_create_team_method(self):
        title = 'test'
        self.manager.create_team(title=title)
        teams_quantity = self.session.query(Team).count()
        self.assertEqual(teams_quantity, 1)

    def test_create_two_teams_with_the_same_title(self):
        title = 'test'
        self.session.add(Team(title=title))
        self.session.commit()

        with self.assertRaises(ManagerException):
            self.manager.create_team(title=title)
            self.session.commit()

    def test_create_project_method(self):
        title = 'test'
        self.manager.create_project(title=title)

        projects_quantity = self.session.query(Project).count()
        self.assertEqual(projects_quantity, 1)

    def test_create_two_projects_with_the_same_title(self):
        title = 'test'
        self.session.add(Project(title=title))
        self.session.commit()

        with self.assertRaises(ManagerException):
            self.manager.create_project(title=title)
            self.session.commit()

    def test_attach_service_group_to_project_method(self):
        title = 'test'
        self.session.add(Project(title=title))
        self.session.add(ServicesGroup(title=title))
        self.session.commit()

        self.manager.attach_service_group_to_project(title, title)
        service_group = self.session.query(ServicesGroup).filter_by(title=title).first()
        self.assertEqual(title, service_group.project.title)

    def test_attach_service_group_to_project_method_when_project_doesnt_exists(self):
        title = 'test'
        self.session.add(ServicesGroup(title=title))
        self.session.commit()

        with self.assertRaises(ManagerException) as context:
            self.manager.attach_service_group_to_project(title, title)

        self.assertEqual(str(context.exception), 'Project with title test doesn\'t exists')

    def test_attach_service_group_to_project_method_when_services_groups_doesnt_exists(self):
        title = 'test'
        self.session.add(Project(title=title))
        self.session.commit()

        with self.assertRaises(ManagerException) as context:
            self.manager.attach_service_group_to_project(title, title)

        self.assertEqual(str(context.exception), 'ServiceGroup with title test doesn\'t exists')

    def test_attach_service_group_to_team_method(self):
        title = 'test'
        self.session.add(Team(title=title))
        self.session.add(ServicesGroup(title=title))
        self.session.commit()

        self.manager.attach_service_group_to_team(title, title)
        service_group = self.session.query(ServicesGroup).filter_by(title=title).first()
        self.assertEqual(title, service_group.team.title)

    def test_attach_service_group_to_team_method_when_team_doesnt_exists(self):
        title = 'test'
        self.session.add(ServicesGroup(title=title))
        self.session.commit()

        with self.assertRaises(ManagerException) as context:
            self.manager.attach_service_group_to_team(title, title)

        self.assertEqual(str(context.exception), 'Team with title test doesn\'t exists')

    def test_attach_service_group_to_team_method_when_service_group_doesnt_exists(self):
        title = 'test'
        self.session.add(Team(title=title))
        self.session.commit()

        with self.assertRaises(ManagerException) as context:
            self.manager.attach_service_group_to_team(title, title)

        self.assertEqual(str(context.exception), 'ServiceGroup with title test doesn\'t exists')

    def test_filter_services_group_by_project(self):
        title = 'test'
        project = Project(title=title)
        self.session.add(project)

        self.session.add_all([ServicesGroup(title='test1', project=project),
                              ServicesGroup(title='test2', project=project),
                              ServicesGroup(title='test3')])
        self.session.commit()

        # self.manager.filter


if __name__ == "__main__":
    unittest.main()
