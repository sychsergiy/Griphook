import os
import pathlib
import json
from griphook.api.formatters import validate_input_cantal_data, format_cantal_data, Metric


BASE_DIR = pathlib.Path(__file__).parents[0]
TEST_DATA_PATH = os.path.join(BASE_DIR, "test_input_data.json")


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


def get_test_data():
    with open(TEST_DATA_PATH) as data_source:
        test_data = data_source.read()
    return test_data
