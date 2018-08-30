from datetime import datetime
from enum import Enum, unique

from sqlalchemy.ext.hybrid import hybrid_property

from griphook.server import bcrypt, db


class Cluster(db.Model):
    __tablename__ = "clusters"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)

    cpu_price = db.Column(db.Float)
    memory_price = db.Column(db.Float)


class Server(db.Model):
    __tablename__ = "servers"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)

    cpu_price = db.Column(db.Float)
    memory_price = db.Column(db.Float)

    cluster_id = db.Column(
        db.Integer, db.ForeignKey(column="clusters.id", name="clusters_fk")
    )


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    created = db.Column(
        db.DateTime, default=datetime.utcnow, server_default=db.func.now()
    )


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    created = db.Column(
        db.DateTime, default=datetime.utcnow, server_default=db.func.now()
    )


class ServicesGroup(db.Model):
    __tablename__ = "services_groups"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)

    project_id = db.Column(
        db.Integer, db.ForeignKey(column="projects.id", name="project_fk", ondelete="SET NULL")
    )

    team_id = db.Column(
        db.Integer, db.ForeignKey(column="teams.id", name="team_fk", ondelete="SET NULL")
    )


class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instance = db.Column(db.String, nullable=False)

    server_id = db.Column(
        db.Integer, db.ForeignKey(column="servers.id", name="servers_fk")
    )

    services_group_id = db.Column(
        db.Integer,
        db.ForeignKey(column="services_groups.id", name="services_group_fk"),
    )

    __table_args__ = (
        db.UniqueConstraint(
            "title", "instance", "services_group_id", "server_id", name="ut_2"
        ),
    )


class BatchStoryPeaks(db.Model):
    __tablename__ = "batches_story_peaks"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, unique=True)
    status = db.Column(db.Integer)
    put_into_queue = db.Column(db.DateTime)


class BatchStoryBilling(db.Model):
    __tablename__ = "batches_story_billing"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, unique=True)
    status = db.Column(db.Integer)
    put_into_queue = db.Column(db.DateTime)


@unique
class MetricTypes(Enum):
    system_cpu_percent = "system_cpu_percent"
    user_cpu_percent = "user_cpu_percent"
    vsize = "vsize"


class MetricPeak(db.Model):
    __tablename__ = "metrics_peaks"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    type = db.Column(db.Enum(MetricTypes, name="peaks_metric_types"))

    batch_id = db.Column(
        db.Integer,
        db.ForeignKey(
            column="batches_story_peaks.id", name="batch_story_peaks_fk"
        ),
    )

    service_id = db.Column(
        db.Integer, db.ForeignKey(column="services.id", name="service_fk")
    )

    services_group_id = db.Column(
        db.Integer,
        db.ForeignKey(column="services_groups.id", name="services_groups_fk"),
    )

    project_id = db.Column(
        db.Integer, db.ForeignKey(column="projects.id", name="projects_fk", ondelete="SET NULL")
    )

    team_id = db.Column(
        db.Integer, db.ForeignKey(column="teams.id", name="teams_fk", ondelete="SET NULL")
    )

    __table_args__ = (
        db.UniqueConstraint(
            "batch_id",
            "type",
            "service_id",
            "services_group_id",
            name="metric_peaks_ut_1",
        ),
    )


class MetricBilling(db.Model):
    __tablename__ = "metrics_billing"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    type = db.Column(db.Enum(MetricTypes, name="billing_metric_types"))

    batch_id = db.Column(
        db.Integer,
        db.ForeignKey(
            column="batches_story_billing.id", name="batch_story_billing_fk"
        ),
    )

    service_id = db.Column(
        db.Integer, db.ForeignKey(column="services.id", name="service_fk")
    )

    services_group_id = db.Column(
        db.Integer,
        db.ForeignKey(column="services_groups.id", name="services_groups_fk"),
    )

    project_id = db.Column(
        db.Integer, db.ForeignKey(column="projects.id", name="projects_fk", ondelete="SET NULL")
    )

    team_id = db.Column(
        db.Integer, db.ForeignKey(column="teams.id", name="teams_fk", ondelete="SET NULL")
    )

    __table_args__ = (
        db.UniqueConstraint(
            "batch_id",
            "type",
            "service_id",
            "services_group_id",
            name="metric_billing_ut_1",
        ),
    )


# Auth models
class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _password = db.Column("password", db.String(255), nullable=False)

    def __init__(self, password, *args, **kwargs):
        self.password = password
        super(Admin, self).__init__(*args, **kwargs)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        new_password = self.validate_password(new_password)
        self._password = bcrypt.generate_password_hash(new_password).decode()

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def validate_password(self, password):
        if not password:
            raise ValueError("Password should be set!")
        if len(password) < 6:
            raise ValueError("Password length should be more than 6 characters")
        return password


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        kwargs.update(defaults or {})
        instance = model(**kwargs)
        session.add(instance)
        return instance, True
