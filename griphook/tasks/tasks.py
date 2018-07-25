from datetime import datetime

from celery import Celery, Task
from celery.utils.log import get_task_logger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from griphook.config.config import Config
from griphook.api.data_source import DataSource
from griphook.api import parsers, formatters
from server.models import (
    Metric,
    MetricType,
    Service,
    ServicesGroup,
    BatchStory
)
from griphook.tasks.utils import (
    DATA_GRANULATION,
    BatchStatus,
    concurrent_get_or_create
)


conf = Config().options
app = Celery(broker=conf['tasks']['CELERY_BROKER_URL'])
logger = get_task_logger(__name__)

engine = create_engine(conf['db']['DATABASE_URL'])
Session = sessionmaker(bind=engine)


class ParsingTask(Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.exception('Parsing metrics failed')

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.retry('Retry parse metrics')


@app.task(base=ParsingTask, time_limit=conf['tasks']['PARSE_METRIC_EXPIRES'])
def parse_metrics(batch_id: int):
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

    try:
        batch = session.query(BatchStory).with_for_update().get(batch_id)

        if batch.status != BatchStatus.STORED:
            time_from = int(batch.time.timestamp())
            time_until = time_from + DATA_GRANULATION - 1

            if time_until <= datetime.now().timestamp():
                logger.info(
                    'Getting data from api (time_from={}; time_until={})'
                    .format(time_from, time_until)
                )
                data = cantal_source.read(time_from=time_from,
                                          time_until=time_until)
                if data is not None:
                    save_metric_to_db(
                        session=session,
                        metrics=data,
                        batch=batch
                    )
                    logger.info('Saved {} metrics'.format(len(data)))
                else:
                    logger.info('Got no data from api')
    except Exception as e:
        session.rollback()
        raise e
    else:
        session.commit()


def save_metric_to_db(session: Session, metrics: formatters.Metric,
                      batch: BatchStory):
    """
    Take parsed metric, save it to database and change batch status to STORED
    """
    for metric_tuple in metrics:
        type_, _ = concurrent_get_or_create(
            session=session,
            model=MetricType,
            title=metric_tuple.type
        )

        services_group, _ = concurrent_get_or_create(
            session=session,
            model=ServicesGroup,
            title=metric_tuple.services_group
        )

        service, _ = concurrent_get_or_create(
            session=session,
            model=Service,
            title=metric_tuple.service,
            services_group=services_group,
            instance=metric_tuple.instance,
            server=metric_tuple.server
        )

        session.add(Metric(
            batch=batch,
            value=metric_tuple.value,
            type=type_,
            service=service
        ))
    batch.status = BatchStatus.STORED
