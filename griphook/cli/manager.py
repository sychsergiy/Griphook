from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from griphook.config.config import Config
from griphook.db.models import Team, Project


def get_session_class():
    config = Config()
    db_url = config.options["db"]["DATABASE_URL"]
    engine = create_engine(db_url)
    return sessionmaker(bind=engine)


Session = get_session_class()


class Manager(object):
    def __init__(self):
        self.session = Session()

    def create_team(self, title):
        instance = Team(title=title)
        self.session.add(instance)
        self.session.commit()
        return instance

    def create_project(self, title):
        instance = Project(title=title)
        self.session.add(instance)
        self.session.commit()

    def __del__(self):
        self.session.close()
