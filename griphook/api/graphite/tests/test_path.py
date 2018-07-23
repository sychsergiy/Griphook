from griphook.api.graphite.target import DotPath


def test_path():
    p = DotPath('foo', 'bar', 'spam')
    assert str(p) == 'foo.bar.spam'
