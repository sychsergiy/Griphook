from typing import List, Any


class Target(object):
    pass


class Path(Target):
    """
    Class for constructing path with custom rules
    Converts every path part to string before joining them

    Example:
            >>> p = Path('foo', 'bar', 'spam')
            >>> str(p)
            >>> 'foo.bar.spam'
    """

    def __init__(self, *chunks: Any, sep: str = '.') -> None:
        self.sep = sep
        self.chunks = list(chunks)

    def __str__(self) -> str:
        """
        Builds string of chunks joined with separator and returns it.
        Any object with __str__ method implemented is suitable
        """
        sep = self.sep
        # Convert every piece of path to str
        chunks = map(str, self.chunks)
        return sep.join(chunks)

    def __iadd__(self, other: Any) -> 'Path':
        """
        Overloaded += operator
        If you are adding Path instance this will extend self.chunks
        with that instance's chunks. Otherwise just append str(instance).
        """
        if isinstance(other, Path):
            self.chunks.extend(other.chunks)
        else:
            self.chunks.append(str(other))

        return self


class MultipleValues(object):
    """
    Graphite API allows to get data from multiple sources in one request
    using curly brace notation, in example:
        'my_server.{my_instance1,my_instance2}.cpu'
    This class defines interface for building that value list

    Example:
        >>> values = GraphiteMultipleValue(values=['foo', bar', 'spam'])
        >>> str(values)
        >>> '{foo,bar,spam}'
    """

    def __init__(self, *, values: List[str]) -> None:
        if not values:
            raise ValueError("values should be non-empty iterable")
        self.values = values

    def __str__(self) -> str:
        """
        Converts each value to string and joins them with comma symbol

        :returns: string of comma-separated values wrapped in curly braces
        """
        values = map(str, self.values)
        return '{{{}}}'.format(','.join(values))
