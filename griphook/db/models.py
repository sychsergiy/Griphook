import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Project(Base):
    __tablename__ = 'projects'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, unique=True)


class ServicesGroup(Base):
    __tablename__ = 'services_groups'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, unique=True)

    project_id = sa.Column(sa.Integer, sa.ForeignKey('projects.id'))
    project = relationship("Project", backref="services_groups")


class Service(Base):
    __tablename__ = 'services'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)
    instance = sa.Column(sa.String)
    server = sa.Column(sa.String)

    services_group_id = sa.Column(sa.Integer, sa.ForeignKey('services_groups.id'))
    services_group = relationship("ServicesGroup", backref="services")

    __table_args__ = (
        sa.UniqueConstraint('title', 'instance', 'services_group_id', 'server'),
    )


class MetricType(Base):
    __tablename__ = 'metric_types'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, unique=True)


class Metric(Base):
    __tablename__ = 'metrics'

    id = sa.Column(sa.Integer, primary_key=True)
    value = sa.Column(sa.Float)
    time_from = sa.Column(sa.TIMESTAMP)

    type_id = sa.Column(sa.Integer, sa.ForeignKey('metric_types.id'))
    type = relationship("MetricType", backref="metrics")

    service_id = sa.Column(sa.Integer, sa.ForeignKey('services.id'))
    service = relationship("Service", backref="metrics")

    __table_args__ = (
        sa.UniqueConstraint(
            'type_id', 'service_id', 'time_from'
        ),
    )


class TaskFlag(Base):
    """
    Store last datetime when was started 
    `griphook.tasks.tasks.parsing_metrics` execution
    """
    __tablename__ = 'task_flags'
    
    id = sa.Column(sa.Integer, primary_key=True)
    datetime = sa.Column(sa.DateTime)


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        kwargs.update(defaults or {})
        instance = model(**kwargs)
        session.add(instance)
        return instance, True