import datetime


def round_time(since, until, step):
    delta = until - since
    m = datetime.timedelta(seconds=delta.total_seconds()) % datetime.timedelta(seconds=step)
    if m:
        until += datetime.timedelta(seconds=step) - m
    return until + datetime.timedelta(days=1)