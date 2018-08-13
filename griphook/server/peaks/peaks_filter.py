from sqlalchemy.orm import Query

from griphook.server.models import (
    MetricPeak,
    BatchStoryPeaks,
    Service,
    ServicesGroup,
    Server,
    Cluster,
)


class MetricPeakGroupFilter(object):
    def __init__(self, session, query: Query = None):
        self.session = session
        self.query = query if query else self.session.query(MetricPeak)
        self.__service_group_joined = False
        self.__service_joined = False
        self.__server_joined = False
        self.__batch_story_joined = False
        self.__cluster_joined = False

    def __join_cluster(self):
        if not self.__cluster_joined:
            self.__join_server()
            self.query = self.query.join(
                Cluster, Server.cluster_id == Cluster.id
            )
            self.__cluster_joined = True

    def __join_server(self):
        if not self.__server_joined:
            if not self.__service_joined:
                self.__join_service()
            self.query = self.query.join(Server)
            self.service_joined = True

    def __join_service(self):
        if not self.__service_joined:
            self.query = self.query.join(Service)
            self.__service_joined = True

    def __join_service_group(self):
        if not self.__service_group_joined:
            if not self.__service_joined:
                self.__join_service()
            self.query = self.query.join(
                ServicesGroup, MetricPeak.services_group_id == ServicesGroup.id
            )
            self.__service_group_joined = True

    def __join_batch_story(self):
        if not self.__batch_story_joined:
            self.query = self.query.join(BatchStoryPeaks)
            self.__batch_story_joined = True

    def filter_by_cluster_id(self, *args: int):
        self.__join_cluster()
        self.query = self.query.filter(Cluster.id.in_(args))

    def filter_by_server_id(self, *args: str):
        self.__join_server()
        self.query = self.query.filter(Server.id.in_(args))
        return self

    def filter_by_service_group_id(self, *args: str):
        self.__join_service_group()
        self.query = self.query.filter(ServicesGroup.id.in_(args))
        return self

    def filter_by_service_id(self, *args: str):
        self.__join_service()
        self.query = self.query.filter(Service.id.in_(args))
        return self

    def filter_by_time_period(self, time_from, time_until):
        self.__join_batch_story()
        self.query = self.query.filter(
            BatchStoryPeaks.time.between(time_from, time_until)
        )
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
