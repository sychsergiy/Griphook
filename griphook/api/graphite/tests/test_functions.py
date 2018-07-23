import pytest
from griphook.api.graphite.functions import Argument, Function
from griphook.api.graphite.target import DotPath, Target


class TestArgument(object):
    def test_string_type(self):
        arg = Argument(str)
        arg.value = 'foo'
        assert str(arg) == '"foo"'

    def test_bool_type(self):
        arg = Argument(bool)
        arg.value = False
        assert str(arg) == 'false'

    def test_non_string(self):
        arg = Argument(float)
        arg.value = 1.5
        assert str(arg) == '1.5'

    def test_arg_is_not_set(self):
        arg = Argument(int)
        with pytest.raises(ValueError):
            str(arg)


class TestFunction(object):
    def test_without_args(self):
        f = Function('sum')
        assert f() == 'sum()'

    def test_one_arg(self):
        f = Function('sum', int)
        assert f(1) == 'sum(1)'

    def test_several_args(self):
        f = Function('sum', int, int, str, bool)
        assert f(0, 1, 'foo', False) == 'sum(0,1,"foo",false)'

    def test_nested_calls(self):
        summarize = Function('summarize', int)
        decrease = Function('decrease', Target, int)
        assert decrease(summarize(5), 2) == 'decrease(summarize(5),2)'


def test_less_arguments_than_specified():
    # last Argument should raise ValueError since value is not set
    with pytest.raises(ValueError):
        summarize = Function('summarize', int, int, int)
        assert summarize(1, 2) == 'summarize(1,2)'


# Integration tests
def test_path_in_function():
    f = Function('summarize', Target, int)
    p = DotPath('foo', 'bar', 'spam')
    assert f(p, 1) == 'summarize(foo.bar.spam,1)'
