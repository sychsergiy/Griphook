from griphook.api.formatters import format_cantal_data, Metric


def get_test_data():
    with open('griphook/api/tests/test_input_data.json', 'r') as data_source:
        test_data = data_source.read()
    return test_data


def test_format_cantal_data():
    test_data = get_test_data()
    result = format_cantal_data(test_data)
    for metric in result:
        assert isinstance(metric, Metric)

    assert len(result) == 8
    assert result[-1].value == 573423616
    assert result[-1].type == 'vsize'
    assert result[-1].services_group == 'galdr--backend'
    assert result[-1].service == 'ua'


def test_format_cantal_data_fail():
    test_data = 'wrong test data'
    result = format_cantal_data(test_data)
    assert result is None
