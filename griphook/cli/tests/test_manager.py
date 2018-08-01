import unittest

from griphook.cli.managers.exceptions import (ProjectManagerException,
                                              TeamManagerException)
from griphook.cli.managers.project import ProjectManager
from griphook.cli.managers.team import TeamManager
from griphook.cli.tests.base import BaseWithDBSession
from griphook.server.models import Project, ServicesGroup, Team


class TeamManagerTestCase(BaseWithDBSession):

    def setUp(self):
        super(TeamManagerTestCase, self).setUp()
        self.manager = TeamManager(self.session)

    def tearDown(self):
        super(TeamManagerTestCase, self).tearDown()

    def test_create_team_method(self):
        title = 'test'
        self.manager.create(title=title)
        teams_quantity = self.session.query(Team).count()
        self.assertEqual(teams_quantity, 1)

    def test_create_two_teams_with_the_same_title(self):
        title = 'test'
        self.session.add(Team(title=title))
        self.session.commit()

        with self.assertRaises(TeamManagerException):
            self.manager.create(title=title)

    def test_attach_service_group_to_team_method(self):
        title = 'test'
        self.session.add(Team(title=title))
        self.session.add(ServicesGroup(title=title))
        self.session.commit()

        self.manager.attach_to_service_group(title, title)
        service_group = self.session.query(ServicesGroup).filter_by(title=title).first()
        self.assertEqual(title, service_group.team.title)

    def test_attach_service_group_to_team_method_when_team_doesnt_exists(self):
        title = 'test'
        self.session.add(ServicesGroup(title=title))
        self.session.commit()

        with self.assertRaises(TeamManagerException) as context:
            self.manager.attach_to_service_group(title, title)

        self.assertEqual(str(context.exception), 'Team with title test doesn\'t exists')

    def test_attach_service_group_to_team_method_when_service_group_doesnt_exists(self):
        title = 'test'
        self.session.add(Team(title=title))
        self.session.commit()

        with self.assertRaises(TeamManagerException) as context:
            self.manager.attach_to_service_group(title, title)

        self.assertEqual(str(context.exception), 'ServiceGroup with title test doesn\'t exists')


class ProjectManagerTestCase(BaseWithDBSession):
    def setUp(self):
        super(ProjectManagerTestCase, self).setUp()
        self.manager = ProjectManager(self.session)
    
    def tearDown(self):
        super(ProjectManagerTestCase, self).tearDown()
    
    def test_create_project_method(self):
        title = 'test'
        self.manager.create(title=title)

        projects_quantity = self.session.query(Project).count()
        self.assertEqual(projects_quantity, 1)

    def test_create_two_projects_with_the_same_title(self):
        title = 'test'
        self.session.add(Project(title=title))
        self.session.commit()

        with self.assertRaises(ProjectManagerException):
            self.manager.create(title=title)

    def test_attach_service_group_to_project_method(self):
        title = 'test'
        self.session.add(Project(title=title))
        self.session.add(ServicesGroup(title=title))
        self.session.commit()

        self.manager.attach_to_service_group(title, title)
        service_group = self.session.query(ServicesGroup).filter_by(title=title).first()
        self.assertEqual(title, service_group.project.title)

    def test_attach_service_group_to_project_method_when_project_doesnt_exists(self):
        title = 'test'
        self.session.add(ServicesGroup(title=title))
        self.session.commit()

        with self.assertRaises(ProjectManagerException) as context:
            self.manager.attach_to_service_group(title, title)

        self.assertEqual(str(context.exception), 'Project with title test doesn\'t exists')

    def test_attach_service_group_to_project_method_when_services_groups_doesnt_exists(self):
        title = 'test'
        self.session.add(Project(title=title))
        self.session.commit()

        with self.assertRaises(ProjectManagerException) as context:
            self.manager.attach_to_service_group(title, title)

        self.assertEqual(str(context.exception), 'ServiceGroup with title test doesn\'t exists')


if __name__ == "__main__":
    unittest.main()
