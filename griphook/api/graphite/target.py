from typing import List


class Target(object):
    pass


class Path(Target):
    def __init__(self, *chunks, sep: str = '.') -> None:
        self.sep = sep
        self.chunks = list(chunks)

    def __str__(self):
        """
        Builds string of chunks joined with separator and returns it.
        Any object with __str__ implemented is suitable
        """
        sep = self.sep
        # chunks = map(str, self.chunks)
        chunks = [str(chunk) for chunk in self.chunks]
        return sep.join(chunks)

    def __repr__(self):
        return self.__str__()

    def __iadd__(self, other: 'Path') -> 'Path':
        self.chunks.extend(other.chunks)
        return self


class GraphiteMultipleValue(object):
    """
    >>> values = GraphiteMultipleValue(values=['foo', bar', 'spam'])
    >>> str(values)
    >>> '{foo,bar,spam}'
    """

    def __init__(self, *, values: List[str]) -> None:
        self.values = values

    def __str__(self):
        return '{{{}}}'.format(','.join(self.values))


if __name__ == "__main__":
    target = Path('foo', 'bar', 'spam')
