import pytest
from griphook.api.graphite.target import MultipleValues


def test_multiple_value_works():
    values = MultipleValues(values=['foo', 'bar', 'spam'])
    assert str(values) == '{foo,bar,spam}'


def test_non_strings():
    values = MultipleValues(values=[1, 2, 3, True, 1.54])
    assert str(values) == '{1,2,3,True,1.54}'


def test_empty_values():
    with pytest.raises(ValueError):
        values = MultipleValues(values=[])
        str(values)
