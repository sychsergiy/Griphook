from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db

Base = declarative_base()


class Metric(Base):
    __tablename__ = 'metrics'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    type = db.Column(db.String)
    services_group = db.Column(db.String)
    service = db.Column(db.String)
    time_from = db.Column(db.Integer)

    def __repr__(self):
        return "<Metric(type={}, value={},)>".format(self.type, self.value)
