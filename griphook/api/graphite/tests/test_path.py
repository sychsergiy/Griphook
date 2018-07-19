from griphook.api.graphite.target import Path

CHUNKS = ['foo', 'bar', 'spam']
DESIRED = '.'.join(CHUNKS)


class S:
    """A class with __str__ method defined"""

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self):
        return self.name


def test_path_works_with_str():
    p = Path('foo', 'bar', 'spam')
    assert str(p) == DESIRED


def test_class_with_str_method():
    s_chunks = [S(c) for c in CHUNKS]
    p = Path(*s_chunks)
    assert str(p) == DESIRED


def test_test_non_str():
    int_arr = range(5)
    p = Path(*int_arr)
    assert str(p) == '0.1.2.3.4'


def test_sep():
    sep = ' MEW '
    p = Path(*CHUNKS, sep=sep)
    assert str(p) == 'foo MEW bar MEW spam'
