from datetime import datetime

from griphook.server.billing.constants import REQUEST_DATE_TIME_FORMAT


def string_to_date_time(time_in_string):
    return datetime.strptime(time_in_string, REQUEST_DATE_TIME_FORMAT)
