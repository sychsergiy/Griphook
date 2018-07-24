import pytest
from griphook.api.graphite.target import MultipleValues


def test_multiple_value_works():
    values = MultipleValues('foo', 'bar', 'spam')
    assert str(values) == '{foo,bar,spam}'


def test_empty_values():
    with pytest.raises(ValueError):
        values = MultipleValues()
        str(values)
