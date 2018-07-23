from datetime import datetime, timedelta

from sqlalchemy.exc import IntegrityError

from griphook.db.models import get_or_create


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
    while True:
        try:
            session.begin_nested()
            obj, created = get_or_create(session, model, defaults, **kwargs)
            session.flush()
        except IntegrityError as e:
            session.rollback()
        else:
            session.commit()
            return obj, created
