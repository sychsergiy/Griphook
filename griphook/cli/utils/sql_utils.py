import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from griphook.db.models import (ServicesGroup, Service, MetricType,
                                Metric)
from griphook.config.config import Config


def create_session():
    config = Config()
    db_url = config.options["db"]["DATABASE_URL"]
    # engine = create_engine('postgres://postgres:postgres@localhost/test1')
    Session = sessionmaker(bind=engine)
    return Session()


def make_query(process, data_type, period):
    session = create_session()
    query = session.query(Metric)\
        .filter(
        ServicesGroup.title == process,
        Metric.time_from.between(period[0], period[1]),
        MetricType.title == data_type)
    results = query.join(MetricType).join(Service).join(ServicesGroup)\
        .order_by(Service.title)\
        .order_by(Metric.time_from)\
        .group_by(Metric.service)\
        .all()

    return results


def all_groups(session):
    return session.query(ServicesGroup.title).distinct(ServicesGroup.title).all()


    # pseudo_now = datetime.datetime(2018, 4, 21, 22)
    # delta = datetime.datetime.now() - datetime.timedelta(days=days, hours=hours)

    # delta = pseudo_now - datetime.timedelta(days=days, hours=hours)

