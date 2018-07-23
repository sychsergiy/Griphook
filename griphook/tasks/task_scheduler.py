import time
import itertools
from datetime import datetime, timedelta
from typing import Sequence

import schedule
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from griphook.config.config import Config
from griphook.db.models import BatchStory
from griphook.tasks.utils import BatchStatus, DATA_GRANULATION, datetime_range
from griphook.tasks import tasks


conf = Config().options
engine = create_engine(conf['db']['DATABASE_URL'])
Session = sessionmaker(bind=engine)

MAX_TASKS = conf['tasks']['MAX_PARSE_TASKS_IN_QUEUE']


def create_batches_until_now():
    """
    Insert batches to db from last batch time or
    from `datetime.now() - conf['tasks']['DATA_SOURCE_DATA_EXPIRES']` if no
    batches in db to `datetime.now()`.
    """
    session = Session()

    now = datetime.now().replace(microsecond=0, second=0, minute=0)
    last_batch = session.query(BatchStory).order_by(
        desc(BatchStory.time)
    ).limit(1).first()
    step = timedelta(seconds=DATA_GRANULATION)

    if last_batch is None:
        time_from = now - \
            timedelta(seconds=conf['tasks']['DATA_SOURCE_DATA_EXPIRES'])
    else:
        time_from = last_batch.time + step

    session.add_all([
        BatchStory(time=batch_time, status=BatchStatus.EMPTY)
        for batch_time in itertools.takewhile(
            lambda t: t < now,
            datetime_range(time_from, now, step)
        )
    ])
    session.commit()


def requeue_expired_batches():
    pass


def push_batches_into_queue(batches: Sequence[BatchStory]):
    """Push batches into queue and set their status to BatchStatus.QUEUED."""
    for batch in batches:
        tasks.parse_metrics.delay(batch_id=batch.id)
        batch.status = BatchStatus.QUEUED


def fill_task_queue():
    """
    Add tasks to queue if batches with status `QUEUED` less than MAX_TASKS
    and there are batches with `EMPTY` status in db.
    """
    session = Session()

    queued_tasks_count = session.query(BatchStory).filter(
        BatchStory.status == BatchStatus.QUEUED
    ).count()

    if queued_tasks_count < MAX_TASKS:
        lack_of_tasks = MAX_TASKS - queued_tasks_count
        batches = session.query(BatchStory).filter(
            BatchStory.status == BatchStatus.EMPTY
        ).limit(lack_of_tasks)

        push_batches_into_queue(batches)
    session.commit()


def main():
    requeue_expired_batches()
    create_batches_until_now()
    fill_task_queue()

    schedule.every(10).minutes.do(requeue_expired_batches)
    schedule.every(15).seconds.do(create_batches_until_now)
    schedule.every(15).seconds.do(fill_task_queue)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
