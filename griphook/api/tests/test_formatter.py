import json
import pathlib

from griphook.api.formatters import (
    Metric,
    format_cantal_data,
    validate_input_cantal_data
)

TEST_DATA_PATH = pathlib.Path(__file__).parent / "test_input_data.json"

# test data for check fields metric object
LAST_METRIC_SERVICES_GROUP = 'galdr--backend'
LAST_METRIC_SERVICE = 'ua'
LAST_METRIC_VALUE = 573423616
LAST_METRIC_TYPE = 'user_cpu_percent'


class TestCantalFormatter:
    def test_validate_input_cantal_data(self):
        test_data = get_test_data()
        decoded_test_data = json.loads(test_data)

        valid_data = validate_input_cantal_data(decoded_test_data)

        for data_series_object in valid_data:
            # check validated data filter
            assert data_series_object is not None

            # check data types validator
            assert isinstance(data_series_object.datapoints, list)
            assert isinstance(data_series_object.datapoints[0], tuple)
            assert isinstance(data_series_object.datapoints[0][0], float)
            assert data_series_object.datapoints[0][0] is not None

            # check metric target validator
            assert 'cantal' in data_series_object.target
            assert 'lithos' in data_series_object.target

    def test_format_cantal_data(self):
        test_data = get_test_data()
        metrics = format_cantal_data(test_data)

        # check fields last metric object
        *_, last_metric = metrics
        assert last_metric.services_group == LAST_METRIC_SERVICES_GROUP
        assert last_metric.service == LAST_METRIC_SERVICE
        assert last_metric.value == LAST_METRIC_VALUE
        assert last_metric.type == LAST_METRIC_TYPE

        # check type metric objects
        for metric in metrics:
            assert isinstance(metric, Metric)


def get_test_data():
    data_source = pathlib.Path(TEST_DATA_PATH)
    test_data = data_source.read_text()
    return test_data
