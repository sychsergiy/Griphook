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

    services_group_id = db.Column(
        db.Integer,
        db.ForeignKey(
            column="services_groups.id",
            name="services_group_fk"
        )
    )
    services_group = db.relationship("ServicesGroup", backref="services")

    __table_args__ = (
        db.UniqueConstraint("title", "instance", "services_group_id", "server",
                            name='ut_2'),
    )


class BatchStory(db.Model):
    __tablename__ = "batches_story"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, unique=True)
    status = db.Column(db.Integer)

    put_into_queue = db.Column(db.DateTime)


class MetricType(db.Model):
    __tablename__ = "metric_types"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)


class Metric(db.Model):
    __tablename__ = "metrics"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)

    batch_id = db.Column(
        db.Integer,
        db.ForeignKey(
            column="batches_story.id",
            name="batch_story_fk"
        )
    )
    batch = db.relationship("BatchStory", backref="metrics")

    type_id = db.Column(
        db.Integer,
        db.ForeignKey(
            column="metric_types.id",
            name="metric_type_fk"
        )
    )
    type = db.relationship("MetricType", backref="metrics")

    service_id = db.Column(
        db.Integer,
        db.ForeignKey(
            column="services.id",
            name="service_fk"
        )
    )
    service = db.relationship("Service", backref="metrics")

    __table_args__ = (
        db.UniqueConstraint(
            "type_id", "service_id", "batch_id", name="ut_1"
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
