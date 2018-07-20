import unittest

from griphook.db.models import Team, Project, ServicesGroup

from griphook.cli.tests.base import BaseWithDBSession
from griphook.cli.filter import ServiceGroupFilter


class ServiceGroupFilterTestCase(BaseWithDBSession):
    def setUp(self):
        self.sv_filter = ServiceGroupFilter(self.session)
        self.clean_up_db()

    def test_filter_by_title(self):
        self.session.add_all([ServicesGroup(title='test1'), ServicesGroup(title='test2'),
                              ServicesGroup(title='test3'), ServicesGroup(title='test4')])
        self.session.commit()

        items = self.sv_filter.filter_by_titles('test1', 'test2', 'another').items()
        self.assertEqual(len(items), 2)

    def test_filter_by_team(self):
        team1 = Team(title='team1')
        team2 = Team(title='team2')
        team3 = Team(title='team3')

        self.session.add_all([team1, team2, team3])
        self.session.add_all([ServicesGroup(title='test1', team=team1), ServicesGroup(title='test2', team=team1),
                              ServicesGroup(title='test3', team=team2), ServicesGroup(title='test4')])
        self.session.commit()

        items = self.sv_filter.filter_by_team_titles('team1', 'team2').items()
        self.assertEqual(len(items), 3)

    def test_filter_by_project(self):
        project1 = Project(title='project1')
        project2 = Project(title='project2')
        project3 = Project(title='project3')

        self.session.add_all([project1, project2, project3])
        self.session.add_all(
            [ServicesGroup(title='test1', project=project1), ServicesGroup(title='test2', project=project1),
             ServicesGroup(title='test3', project=project2), ServicesGroup(title='test4')])
        self.session.commit()

        items = self.sv_filter.filter_by_project_titles('project1', 'project2').items()
        self.assertEqual(len(items), 3)

    # integration test
    def test_chain_filter_by_team_project_title(self):
        team1 = Team(title='team1')
        team2 = Team(title='team2')
        team3 = Team(title='team3')

        project1 = Project(title='project1')
        project2 = Project(title='project2')
        project3 = Project(title='project3')

        self.session.add_all([project1, project2, project3])
        self.session.add_all(
            [ServicesGroup(title='test1', project=project1, team=team1), ServicesGroup(title='test2', project=project1),
             ServicesGroup(title='test3', project=project2), ServicesGroup(title='test4')])

        self.session.add_all([team1, team2, team3])
        self.session.add_all(
            [ServicesGroup(title='test5', project=project2, team=team1), ServicesGroup(title='test6', team=team1),
             ServicesGroup(title='test7', team=team2), ServicesGroup(title='test8')])
        self.session.commit()

        items = self.sv_filter.filter_by_project_titles('project1', 'project2') \
            .filter_by_team_titles('team1', 'team2') \
            .filter_by_titles('test1', 'test3', 'test5', 'test7', 'test9').items()

        self.assertEqual(len(items), 2)


if __name__ == "__main__":
    unittest.main()
