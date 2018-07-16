from collections import OrderedDict
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from griphook.db.models import (ServicesGroup, Service, MetricType,
                                Metric)
from griphook.config.config import Config


def make_query(process, type, days, hours):
    config = Config()
    db_URL = config.options["db"]["DATABASE_URL"]
    engine = create_engine(db_URL)

    # pseudo_now = datetime.datetime(2018, 4, 21, 22)
    delta = datetime.datetime.now() - datetime.timedelta(days=days, hours=hours)

    # delta = pseudo_now - datetime.timedelta(days=days, hours=hours)

    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Metric).join(MetricType).join(Service).join(ServicesGroup)
    results = query.filter(
        ServicesGroup.title == process,
        Metric.time_from > delta,
        MetricType.title == type)\
        .order_by(Service.title)\
        .order_by(Metric.time_from)\
        .all()

    return results


def metric_data(metrics):
    for metric in metrics:
        yield OrderedDict([
            ('Server', metric.service.server),
            ('Process', metric.service.services_group.title),
            ('Service', metric.service.title),
            ('Instance', metric.service.instance),
            ('Date/Time', metric.time_from),
            ('Metric Type', metric.type.title),
            ('Value', metric.value),
        ])
