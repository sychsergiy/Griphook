import datetime

from sqlalchemy import func
from sqlalchemy.orm import Query

from griphook.server.models import MetricPeak, BatchStoryPeaks, Service, ServicesGroup, Server
from griphook.server import db


def round_time(since, until, step):
    delta = until - since
    modular = datetime.timedelta(seconds=delta.total_seconds()) % datetime.timedelta(seconds=step)
    if modular:
        until += datetime.timedelta(seconds=step) - modular
    return until


class MetricPeakGroupFilter(object):
    def __init__(self, session, query: Query = None):
        self.session = session
        self.query = query if query else self.session.query(MetricPeak)
        self.service_group_joined = False
        self.service_joined = False
        self.server_joined = False
        self.batch_story_joined = False

    def __join_service(self):
        if not self.service_joined:
            self.query = self.query.join(Service)
            self.service_joined = True

    def __join_server(self):
        if not self.server_joined:
            if not self.service_joined:
                self.__join_service()
            self.query = self.query.join(Server)
            self.service_joined = True

    def __join_service_group(self):
        if not self.service_group_joined:
            if not self.service_joined:
                self.__join_service()
            self.query = self.query.join(ServicesGroup, MetricPeak.services_group_id == ServicesGroup.id)
            self.service_group_joined = True

    def __join_batch_story(self):
        if not self.batch_story_joined:
            self.query = self.query.join(BatchStoryPeaks)
            self.batch_story_joined = True

    def filter_by_server_title(self, *args: str):
        self.__join_server()
        self.query = self.query.filter(Server.title.in_(args))
        return self

    def filter_by_service_group_title(self, *args: str):
        self.__join_service_group()
        self.query = self.query.filter(ServicesGroup.title.in_(args))
        return self

    def filter_by_service_title(self, *args: str):
        self.__join_service()
        self.query = self.query.filter(Service.title.in_(args))
        return self

    def filter_by_time_period(self, since, until):
        self.__join_batch_story()
        self.query = self.query.filter(BatchStoryPeaks.time.between(since, until))
        return self

    def filter_by_metric_type(self, *args: str):
        self.query = self.query.filter(MetricPeak.type.in_(args))
        return self

    def set_query_entities(self, *args):
        self.query = self.query.with_entities(*args)
        return self

    def group_by(self, *args: str):
        self.query = self.query.group_by(*args)
        return self

    def order_by(self, label: str):
        self.query = self.query.order_by(label)
        return self

    def get_items(self):
        return self.query.all()


def get_shift(since, step):
    since_timestamp = since.replace(tzinfo=datetime.timezone.utc).timestamp()
    return since_timestamp % step


def peaks_query(query_data):
    server = query_data.get('server')
    since = query_data.get('since')
    until = query_data.get('until')
    step = query_data.get('step')
    metric_type = query_data.get('metric_type')
    service = query_data.get('service')
    service_group = query_data.get('service_group')
    until = round_time(since, until, step=step)
    shift = get_shift(since, step)
    group_time = (func.floor((func.extract('epoch', BatchStoryPeaks.time) - shift) / step)) * step
    query_creator = MetricPeakGroupFilter(session=db.session)
    (
        query_creator
        .filter_by_metric_type(metric_type)
        .filter_by_time_period(since=since, until=until)
        .filter_by_server_title(server)
        .set_query_entities(
            func.max(MetricPeak.value).label("peaks"),
            group_time.label('step'),
            func.min(func.extract('epoch', BatchStoryPeaks.time)).label('time'),
            MetricPeak.type.label('type')
        )
        .group_by('step', 'type')
        .order_by('time')
    )
    if service_group:
        query_creator.filter_by_service_group_title(service_group)
        if service:
            query_creator.filter_by_service_title(service)
    return query_creator.query


def peak_formatter(peak):
    return (
        datetime.datetime.fromtimestamp(
            peak.time,
            tz=datetime.timezone.utc
        ).strftime('%Y-%m-%d %H')
    )


def validate_peaks_query(args):
    date_time_format = '%Y-%m-%d %H'
    data = dict()
    error_data = dict()
    try:
        data['step'] = int(args.get('step'))
    except TypeError:
        error_data = {'Error': "Error step field is required"}
    except ValueError:
        error_data = {'Error': "Error step format. Expected int"}
    try:
        data['since'] = datetime.datetime.strptime(args.get('since'), date_time_format)
        data['until'] = datetime.datetime.strptime(args.get('until'), date_time_format)
    except TypeError:
        error_data = {'Error': "since and until are required fields"}
    except ValueError:
        error_data = {'Error': "Error datetime (since or until) format. Expected {0}".format(date_time_format)}
    data['service_group'] = args.get('services_group')
    data['service'] = args.get('service')
    data['metric_type'] = args.get('metric_type')
    data['server'] = args.get('server')
    if not data['metric_type'] or not data['server']:
        error_data = {'Error': "metric_type and server are required fields"}
    return data, error_data
