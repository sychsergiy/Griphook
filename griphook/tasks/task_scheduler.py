import time
import itertools
from datetime import datetime, timedelta
from typing import Sequence

import schedule
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from griphook.config import Config
from griphook.server.models import BatchStoryPeaks, BatchStoryBilling
from griphook.tasks.utils import (
    BatchStatus,
    DATA_GRANULATION,
    datetime_range
)
from griphook.tasks import tasks


conf = Config().options
engine = create_engine(conf["db"]["DATABASE_URL"])
Session = sessionmaker(bind=engine)

MAX_TASKS = conf["tasks"]["MAX_PARSE_TASKS_IN_QUEUE"]
DATA_SOURCE_DATA_EXPIRES = conf["tasks"]["DATA_SOURCE_DATA_EXPIRES"]
PARSE_METRIC_EXPIRES = conf["tasks"]["PARSE_METRIC_EXPIRES"]
CREATING_BATCHES_INTERVAL = conf["tasks"]["CREATING_BATCHES_INTERVAL"]
FILLING_TASK_QUEUE_INTERVAL = conf["tasks"]["FILLING_TASK_QUEUE_INTERVAL"]


class TaskScheduler(object):

    def __init__(self, batch_model, task):
        self._session = Session()
        self._batch_model = batch_model
        self._task = task

    def create_batches_until_now(self):
        """
        Insert batches to db from last batch time or
        from `datetime.now() - conf['tasks']['DATA_SOURCE_DATA_EXPIRES']` if no
        batches in db to `datetime.now()`.
        """
        now = datetime.now().replace(microsecond=0, second=0, minute=0)
        last_batch = (
            self._session.query(self._batch_model)
            .order_by(desc(self._batch_model.time))
            .limit(1)
            .first()
        )
        step = timedelta(seconds=DATA_GRANULATION)

        if last_batch is None:
            time_from = now - \
                timedelta(seconds=DATA_SOURCE_DATA_EXPIRES)
        else:
            time_from = last_batch.time + step

        self._session.add_all([
            self._batch_model(time=batch_time, status=BatchStatus.EMPTY)
            for batch_time in itertools.takewhile(
                lambda t: t < now,
                datetime_range(time_from, now, step)
            )
        ])
        self._session.commit()

    def requeue_expired_batches(self):
        """Put expired batches to the tasks queue again"""
        expired_batches = (
            self._session.query(self._batch_model)
            .filter(self._batch_model.put_into_queue < datetime.now() -
                    timedelta(seconds=PARSE_METRIC_EXPIRES),
                    self._batch_model.status == BatchStatus.QUEUED)
            .all()
        )

        self._push_batches_into_queue(expired_batches)

    def _push_batches_into_queue(self, batches: Sequence[BatchStoryPeaks]):
        """Push batches into queue and set their status to BatchStatus.QUEUED."""
        for batch in batches:
            batch.put_into_queue = datetime.now()
            batch.status = BatchStatus.QUEUED
        self._session.commit()

        for batch in batches:
            self._task.delay(batch_id=batch.id)

    def fill_task_queue(self):
        """
        Add tasks to queue if batches with status `QUEUED` less than MAX_TASKS
        and there are batches with `EMPTY` status in db.
        """
        queued_tasks_count = (
            self._session.query(self._batch_model)
            .filter(self._batch_model.status == BatchStatus.QUEUED)
            .count()
        )

        if queued_tasks_count < MAX_TASKS:
            lack_of_tasks = MAX_TASKS - queued_tasks_count
            batches = (
                self._session.query(self._batch_model)
                .filter(self._batch_model.status == BatchStatus.EMPTY)
                .limit(lack_of_tasks)
                .all()
            )

            self._push_batches_into_queue(batches)
        self._session.commit()

    def fill_schedule(self, schedule: schedule, start_now=True):
        if start_now:
            self.requeue_expired_batches()
            self.create_batches_until_now()
            self.fill_task_queue()

        schedule.every(
            DATA_GRANULATION
        ).seconds.do(self.requeue_expired_batches)

        schedule.every(
            CREATING_BATCHES_INTERVAL
        ).seconds.do(self.create_batches_until_now)

        schedule.every(
            FILLING_TASK_QUEUE_INTERVAL
        ).seconds.do(self.fill_task_queue)


def main():
    peaks_parsing_scheduler = TaskScheduler(
        batch_model=BatchStoryPeaks,
        task=tasks.parse_peak_metrics
    )
    peaks_parsing_scheduler.fill_schedule(schedule)

    average_parsing_scheduler = TaskScheduler(
        batch_model=BatchStoryBilling,
        task=tasks.parse_average_metrics
    )
    average_parsing_scheduler.fill_schedule(schedule)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
