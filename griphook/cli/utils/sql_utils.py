import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from griphook.config.config import Config
from griphook.db.models import Metric, MetricType, Service, ServicesGroup


def make_query(process, data_type, period):
    config = Config()
    db_url = config.options["db"]["DATABASE_URL"]
    engine = create_engine(db_url)

    # pseudo_now = datetime.datetime(2018, 4, 21, 22)
    # delta = datetime.datetime.now() - datetime.timedelta(days=days, hours=hours)

    # delta = pseudo_now - datetime.timedelta(days=days, hours=hours)

    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Metric).filter(
        ServicesGroup.title == process,
        Metric.time_from.between(period[0], period[1]),
        MetricType.title == data_type)
    results = query.join(MetricType).join(Service).join(ServicesGroup)\
        .order_by(Service.title)\
        .order_by(Metric.time_from)\
        .all()

    return results
