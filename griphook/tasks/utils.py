from datetime import datetime, timedelta

from sqlalchemy.exc import IntegrityError


# Changing this variable if there is some data in database
# may occur data corruption
DATA_GRANULATION = 3600


class BatchStatus(object):
    EMPTY = 1
    QUEUED = 2
    STORED = 3


def datetime_range(start: datetime, end: datetime, step: timedelta):
    while start < end:
        yield start
        start += step


def concurrent_get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        try:
            session.begin_nested()
            kwargs.update(defaults or {})
            instance = model(**kwargs)
            session.add(instance)
            session.commit()
        except IntegrityError:
            session.rollback()
            return session.query(model).filter_by(**kwargs).first(), False
        return instance, True
