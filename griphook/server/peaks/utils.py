import datetime

from sqlalchemy import func

from griphook.server import db
from griphook.server.models import MetricPeak, BatchStoryPeaks
from griphook.server.peaks.peaks_filter import MetricPeakGroupFilter


def round_time(since, until, step):
    """
    checking whether the step fits into the time delta without the remainder.
    If it doesn't, extends the the time_until for delta to be fully divisible by the step.
    """
    delta = until - since
    modular = datetime.timedelta(
        seconds=delta.total_seconds()
    ) % datetime.timedelta(seconds=step)
    if modular:
        until += datetime.timedelta(seconds=step) - modular
    return until


def get_shift(since, step):

    """
    UNIX timestamp divided by the step into intervals that synchronize with the time_from
    """
    since_timestamp = since.replace(tzinfo=datetime.timezone.utc).timestamp()
    return since_timestamp % step


def get_peaks_query_group_by_time_step(
    target_type, target_id, step, metric_type, time_from, time_until
):
    time_until = round_time(time_from, time_until, step=step)
    shift = get_shift(time_from, step)
    group_time = (
        func.floor((func.extract("epoch", BatchStoryPeaks.time) - shift) / step)
    ) * step
    query_creator = MetricPeakGroupFilter(session=db.session)
    (
        query_creator.filter_by_metric_type(metric_type)
        .filter_by_time_period(time_from=time_from, time_until=time_until)
        .set_query_entities(
            func.max(MetricPeak.value).label("peaks"),
            group_time.label("step"),
            func.min(func.extract("epoch", BatchStoryPeaks.time)).label("time"),
            MetricPeak.type.label("type"),
        )
        .group_by("step", "type")
        .order_by("time")
    )
    if target_type == "cluster":
        query_creator.filter_by_cluster_id(target_id)
    elif target_type == "server":
        query_creator.filter_by_server_id(target_id)
    elif target_type == "services_group":
        query_creator.filter_by_service_group_id(target_id)
    elif target_type == "service":
        query_creator.filter_by_service_id(target_id)
    return query_creator


def peak_formatter(peak):
    return datetime.datetime.fromtimestamp(
        peak.time, tz=datetime.timezone.utc
    ).strftime("%Y-%m-%d")


def validate_peaks_query(validation_data):
    valid_target_types = ("service", "services_group", "server", "cluster")
    date_time_format = "%Y-%m-%d"
    data = dict()
    error_data = dict()
    try:
        data["step"] = int(validation_data.get("step"))
    except TypeError:
        error_data = {"error": "Error step field is required"}
    except ValueError:
        error_data = {"error": "Error step format. Expected int"}
    try:
        data["time_from"] = datetime.datetime.strptime(
            validation_data.get("time_from"), date_time_format
        )
        data["time_until"] = datetime.datetime.strptime(
            validation_data.get("time_until"), date_time_format
        )
    except TypeError:
        error_data = {"error": "time_from and time_until are required fields"}
    except ValueError:
        error_data = {
            "error": "Error datetime (time_from or time_until) format. Expected {0}".format(
                date_time_format
            )
        }
    data["target_type"] = validation_data.get("target_type")
    data["target_id"] = validation_data.get("target_id")
    data["metric_type"] = validation_data.get("metric_type")
    if not data["metric_type"]:
        error_data = {"error": "metric_type is required field"}
    elif not data["target_type"] in valid_target_types:
        error_data = {"error": "target_type is required field"}
    elif not data["target_id"]:
        error_data = {"error": "target_id is required field"}
    return data, error_data
