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
    title = sa.Column(sa.String, unique=True)

    services_group_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(
            'services_groups.id'
        )
    )
    services_group = relationship("ServicesGroup", backref="services")


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
