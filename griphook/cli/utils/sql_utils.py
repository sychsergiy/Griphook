import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from griphook.db.models import (ServicesGroup, Service, MetricType,
                                Metric, BatchStory)
from griphook.config.config import Config


def create_session():
    config = Config()
    db_url = config.options["db"]["DATABASE_URL"]
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session()


def make_query(session, process, data_type, since, until=None, group=False):
    if not until:
        until = datetime.datetime.now()
    query = (
        session.query(Metric)
        .join(MetricType, Service, ServicesGroup)
        .filter(
        ServicesGroup.title == process,
        BatchStory.time.between(since, until),
        MetricType.title == data_type)
        .join(MetricType).join(Service).join(ServicesGroup)
        .order_by(Service.title)
        .order_by(BatchStory.time).all()
    )

    return query



def all_groups(session):
    return session.query(ServicesGroup).distinct(ServicesGroup.title)





