from datetime import datetime


def modify_time(raw_date):
    if raw_date:
        return datetime.strptime(raw_date, '%Y-%m-%d')
    return None


def raw_output_formatter(row):
    return row.service_group, row.metric_type.value, row.value

