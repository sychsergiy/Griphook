from datetime import datetime

from celery import Celery, Task
from celery.utils.log import get_task_logger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError

from griphook.config import Config
from griphook.api.data_source import DataSource

from griphook.api.graphite import (
    parser as parsers, 
    formatters,
    functions as graphite_api_functions
)
from griphook.server.models import (
    BatchStoryPeaks,
    BatchStoryBilling,
    MetricTypes,
    Service,
    ServicesGroup,
    MetricPeak,
    MetricBilling,
    Cluster,
    Server
)
from griphook.tasks.utils import (
    DATA_GRANULATION,
    BatchStatus,
    concurrent_get_or_create
)

import urllib3
urllib3.disable_warnings()


conf = Config().options
app = Celery(broker=conf['tasks']['CELERY_BROKER_URL'])
logger = get_task_logger(__name__)

engine = create_engine(conf['db']['DATABASE_URL'])
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)


def base_parse_metrics(batch_model, batch_id, parser, target, format_func,
                       metric_model):
    session = Session()
    batch = session.query(batch_model).with_for_update().get(batch_id)

    if batch is not None and batch.status == BatchStatus.QUEUED:
        time_from = int(batch.time.timestamp())
        time_until = time_from + DATA_GRANULATION - 1

        # We parse metrics only for the past time
        if time_until <= datetime.now().timestamp():
            logger.info(
                'Getting data from api <time_from=`{}` time_until=`{}` batch_model=`{}` batch_id=`{}`>'
                .format(datetime.fromtimestamp(time_from), 
                        datetime.fromtimestamp(time_until),
                        batch_model.__name__,
                        batch_id)
            )

            data = format_func(parser.fetch(
                time_from=time_from,
                time_until=time_until,
                target=target
            ))
            try:
                data_count = save_metric_to_db(
                    session=session,
                    metrics=data,
                    batch=batch,
                    metric_model=metric_model
                )
            except IntegrityError:
                session.rollback()
                logger.warning(
                    'Database already had data for batch_id={}'.format(batch_id)
                )
                batch.status = BatchStatus.STORED
            else:    
                logger.info('Saved {} metrics'.format(data_count))
        else:
            logger.warning(
                'Got broken batch - time_until > datetime.now (batch_id=`{}`)'
                .format(batch_id)
            )

    session.commit()


@app.task(time_limit=conf['tasks']['PARSE_METRIC_EXPIRES'])
def parse_peak_metrics(batch_id: int):
    batch_model = BatchStoryPeaks
    metric_model = MetricPeak
    parser = parsers.GraphiteAPIParser(base_url=conf['api']['GRAPHITE_URL'])
    target = parsers.GraphiteAPIParser.construct_target(
        function=graphite_api_functions.summarize,
        func_args=("1hour", "max", True)
    )
    format_func = formatters.format_cantal_data

    base_parse_metrics(
        batch_model=batch_model,
        batch_id=batch_id,
        parser=parser,
        target=target,
        format_func=format_func,
        metric_model=metric_model
    )


@app.task(time_limit=conf['tasks']['PARSE_METRIC_EXPIRES'])
def parse_average_metrics(batch_id: int):
    batch_model = BatchStoryBilling
    metric_model = MetricBilling
    parser = parsers.GraphiteAPIParser(base_url=conf['api']['GRAPHITE_URL'])
    target = parsers.GraphiteAPIParser.construct_target(
        function=graphite_api_functions.summarize,
        func_args=("1hour", "avg", True)
    )
    format_func = formatters.format_cantal_data

    base_parse_metrics(
        batch_model=batch_model,
        batch_id=batch_id,
        parser=parser,
        target=target,
        format_func=format_func,
        metric_model=metric_model
    )    


def save_metric_to_db(session, metrics, batch, metric_model) -> int:
    """
    Take parsed metric, save it to database and change batch status to STORED
    """
    rel_data_session = Session()
    counter = 0
    for metric_tuple in metrics:
        counter += 1
        type_ = MetricTypes(metric_tuple.type)

        services_group, _ = concurrent_get_or_create(
            session=rel_data_session,
            model=ServicesGroup,
            title=metric_tuple.services_group
        )

        cluster, _ = concurrent_get_or_create(
            session=rel_data_session,
            model=Cluster,
            title=metric_tuple.cluster
        )

        server, _ = concurrent_get_or_create(
            session=rel_data_session,
            model=Server,
            title=metric_tuple.server,
            cluster_id=cluster.id
        )

        service, _ = concurrent_get_or_create(
            session=rel_data_session,
            model=Service,
            title=metric_tuple.service,
            services_group_id=services_group.id,
            instance=metric_tuple.instance,
            server_id=server.id
        )

        session.add(metric_model(
            batch_id=batch.id,
            value=metric_tuple.value,
            type=type_,
            service_id=service.id,
            services_group_id=services_group.id
        ))
    batch.status = BatchStatus.STORED
    return counter
