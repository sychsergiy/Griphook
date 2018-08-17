import pytest

from griphook.api.graphite.target import DotPath


@pytest.fixture
def path():
    return DotPath("foo", "bar", "spam")


@pytest.fixture
def empty_path():
    return DotPath()


@pytest.fixture
def desired_path_str():
    return "foo.bar.spam.eggs"


def test_path(path, desired_path_str):
    assert str(DotPath("foo", "bar", "spam", "eggs")) == desired_path_str


def test_empty_path(empty_path):
    assert str(empty_path) == ""


def test_add_string(path, desired_path_str):
    assert str(path + "eggs") == desired_path_str


def test_add_path(desired_path_str):
    res = DotPath("foo", "bar") + DotPath("spam", "eggs")
    assert str(res) == desired_path_str


def test_empty_add(empty_path):
    assert str(empty_path + "eggs") == "eggs"


def test_iadd(path, desired_path_str):
    path += "eggs"
    assert str(path) == desired_path_str
