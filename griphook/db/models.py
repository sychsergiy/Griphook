from enum import Enum, unique
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Team(Base):
    __tablename__ = "teams"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, unique=True)
    created = sa.Column(
        sa.DateTime,
        default=datetime.utcnow,
        server_default=sa.func.now()
    )


class Project(Base):
    __tablename__ = "projects"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, unique=True)
    created = sa.Column(
        sa.DateTime,
        default=datetime.utcnow,
        server_default=sa.func.now()
    )


class ServicesGroup(Base):
    __tablename__ = "services_groups"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, unique=True)

    project_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(
            column="projects.id",
            name="project_fk"
        )
    )
    project = relationship("Project", backref="services_groups")

    team_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(
            column="teams.id",
            name="team_fk"
        )
    )
    team = relationship("Team", backref="services_groups")


class Service(Base):
    __tablename__ = "services"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)
    instance = sa.Column(sa.String)
    server = sa.Column(sa.String)
    cluster = sa.Column(sa.String)

    services_group_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(
            column="services_groups.id",
            name="services_group_fk"
        )
    )
    services_group = relationship("ServicesGroup", backref="services")

    __table_args__ = (
        sa.UniqueConstraint(
            "title", "instance", "services_group_id", "server", name='ut_2'
        ),
    )


class BatchStory(Base):
    __tablename__ = "batches_story"

    id = sa.Column(sa.Integer, primary_key=True)
    time = sa.Column(sa.DateTime, unique=True)
    status = sa.Column(sa.Integer)
    put_into_queue = sa.Column(sa.DateTime)


@unique
class MetricTypes(Enum):
    system_cpu_percent = "system_cpu_percent"
    user_cpu_percent = "user_cpu_percent"
    vsize = "vsize"


class Metric(Base):
    __tablename__ = "metrics"

    id = sa.Column(sa.Integer, primary_key=True)
    value = sa.Column(sa.Float)
    type = sa.Column(sa.Enum(MetricTypes))

    batch_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(
            column="batches_story.id",
            name="batch_story_fk"
        )
    )
    batch = relationship("BatchStory", backref="metrics")

    service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(
            column="services.id",
            name="service_fk"
        )
    )
    service = relationship("Service", backref="metrics")

    services_group_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(
            column="services_groups.id",
            name="services_groups_fk"
        )
    )
    services_group = relationship("ServicesGroup", backref="metrics")

    project_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(
            column="projects.id",
            name="projects_fk"
        )
    )
    project = relationship("Project", backref="metrics")

    team_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(
            column="teams.id",
            name="teams_fk"
        )
    )
    team = relationship("Team", backref="metrics")

    __table_args__ = (
        sa.UniqueConstraint(
            "batch_id", "type", "service_id", "services_group_id", name="ut_1"
        ),
    )


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        kwargs.update(defaults or {})
        instance = model(**kwargs)
        session.add(instance)
        return instance, True
