from enum import Enum, unique
from datetime import datetime

from griphook.server import db


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    created = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        server_default=db.func.now()
    )


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    created = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        server_default=db.func.now()
    )


class ServicesGroup(db.Model):
    __tablename__ = "services_groups"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)

    project_id = db.Column(
        db.Integer,
        db.ForeignKey(
            column="projects.id",
            name="project_fk"
        )
    )
    project = db.relationship("Project", backref="services_groups")

    team_id = db.Column(
        db.Integer,
        db.ForeignKey(
            column="teams.id",
            name="team_fk"
        )
    )
    team = db.relationship("Team", backref="services_groups")


class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    instance = db.Column(db.String)
    server = db.Column(db.String)
    cluster = db.Column(db.String)

    services_group_id = db.Column(
        db.Integer,
        db.ForeignKey(
            column="services_groups.id",
            name="services_group_fk"
        )
    )
    services_group = db.relationship("ServicesGroup", backref="services")

    __table_args__ = (
        db.UniqueConstraint(
            "title", "instance", "services_group_id", "server", name='ut_2'
        ),
    )


class BatchStory(db.Model):
    __tablename__ = "batches_story"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, unique=True)
    status = db.Column(db.Integer)
    put_into_queue = db.Column(db.DateTime)


@unique
class MetricTypes(Enum):
    system_cpu_percent = "system_cpu_percent"
    user_cpu_percent = "user_cpu_percent"
    vsize = "vsize"


class Metric(db.Model):
    __tablename__ = "metrics"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    type = db.Column(db.Enum(MetricTypes))

    batch_id = db.Column(
        db.Integer,
        db.ForeignKey(
            column="batches_story.id",
            name="batch_story_fk"
        )
    )
    batch = db.relationship("BatchStory", backref="metrics")

    service_id = db.Column(
        db.Integer,
        db.ForeignKey(
            column="services.id",
            name="service_fk"
        )
    )
    service = db.relationship("Service", backref="metrics")

    services_group_id = db.Column(
        db.Integer,
        db.ForeignKey(
            column="services_groups.id",
            name="services_groups_fk"
        )
    )
    services_group = db.relationship("ServicesGroup", backref="metrics")

    project_id = db.Column(
        db.Integer,
        db.ForeignKey(
            column="projects.id",
            name="projects_fk"
        )
    )
    project = db.relationship("Project", backref="metrics")

    team_id = db.Column(
        db.Integer,
        db.ForeignKey(
            column="teams.id",
            name="teams_fk"
        )
    )
    team = db.relationship("Team", backref="metrics")

    __table_args__ = (
        db.UniqueConstraint(
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