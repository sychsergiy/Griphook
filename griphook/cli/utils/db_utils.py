from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from griphook.config.config import Config


def get_session_class():
    config = Config()
    db_url = config.options["db"]["DATABASE_URL"]
    engine = create_engine(db_url)
    return sessionmaker(bind=engine)
