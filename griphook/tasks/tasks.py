import os
from datetime import datetime

from celery import Celery
from celery import Task
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from sqlalchemy import select

from griphook.config.config import Config
from griphook.api.data_source import DataSource
from griphook.api import parsers, formatters
from griphook.db.models import Metric


conf = Config().options
app = Celery(broker_url=conf['tasks']['CELERY_BROKER_URL'])
logger = get_task_logger(__name__)

engine = create_engine(conf['db']['DATABASE_URL'])
if not engine.dialect.has_table(engine, Metric.__tablename__):
    Metric.__table__.create(engine)
Session = sessionmaker(bind=engine)


@periodic_task(
    run_every=conf['tasks']['TRYING_SETUP_PARSER_INTERVAL'],
    name='start_parser',
    ignore_result=True
)
def start_parser():
    """
    Celery beat task.
    Start parser according to schedule
    """
    parse_metrics.delay()


class ParsingTask(Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.exception('Parsing metrics failed')

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.retry('Retry parse metrics')


@app.task(base=ParsingTask)
def parse_metrics():
    """
    Parse data from Cantal API and save it to specified in Session db.
    This task should be executed only by one worker at the same time.
    :TODO
        Change task to parse data from different API's
    """
    session = Session()
    cantal_source = DataSource(
        parser=parsers.GraphiteAPIParser(base_url=conf['api']['GRAPHITE_URL']),
        data_formatter=formatters.format_cantal_data,
    )

    # Get row with last timestamp in db and calculate time_from and time_until
    row = session.execute(
        select([Metric.time_from]).order_by(desc(Metric.time_from)).limit(1)
    ).first()
    if row is not None:
        time_from = int(row.time_from.timestamp()) + conf['tasks']['DATA_GRANULATION']
    else:
        rounded_now = datetime.now().replace(microsecond=0,second=0,minute=0)
        time_from = int(rounded_now.timestamp()) - conf['tasks']['DATA_SOURCE_DATA_EXPIRES']
    time_until = time_from + conf['tasks']['DATA_GRANULATION']

    if time_until <= datetime.now().timestamp():
        logger.info('Getting data from api (time_from={}; time_until={})'.format(time_from, time_until))
        data = cantal_source.read(time_from=time_from, time_until=time_until)
        if data:
            # Generate db Metric objects and save to db
            session.add_all([
                Metric(**metric._asdict(), time_from=datetime.fromtimestamp(time_from)) for metric in data
            ])
            session.commit()
            logger.info('Saved {} metrics'.format(len(data)))
        else:
            logger.info('Got no data from api')

        parse_metrics.delay()
