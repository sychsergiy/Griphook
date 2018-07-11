import os

from celery import Celery
from celery import Task
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

import celeryconfig as conf


app = Celery(broker_url=os.environ.get('CELERY_BROKER_URL'))
logger = get_task_logger(__name__)


@periodic_task(
    run_every=conf.TRYING_SETUP_PARSER_INTERVAL,
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
        logger.warning('Parsing metrics failed')

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.retry('Retry parse metrics')


@app.task(base=ParsingTask)
def parse_metrics():
    """
    :TODO
        1. Calculate `from` and `until` timestamps using last metric in DB and timedelta between
           metrics.
           If there is no metric in db, set `from` to
           datetime.datetime.now() - DATA_SOURCE_DATA_EXPIRES,
           where DATA_SOURCE_DATA_EXPIRES -> how long data in data source is saved

        2. Using calculated `from` and `until` timestamps - get metric.

        3. Save metric in DB

        4. If `until` + `timedelta between metrics` < datetime.datetime.now() -> Start task again
    """
    pass
