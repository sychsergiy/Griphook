from typing import Any


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

    def __init__(self, *chunks: Any) -> None:
        # Validation of chunks
        self.chunks = list(chunks)

    def __str__(self) -> str:
        """
        Builds string of chunks joined with separator and returns it.
        Any object with __str__ method implemented is suitable
        """
        # Convert every piece of path to str
        return '.'.join(map(str, self.chunks))

    def __add__(self, other: Any) -> 'Path':
        """
        Overloaded plus operator

        :returns: Path object with copy of chunks from both operands
        """
        chunks = self.chunks.copy()
        if isinstance(other, Path):
            chunks += other.chunks
        else:
            chunks.append(str(other))

        return Path(*chunks)


class MultipleValues(object):
    """
    Graphite API allows to get data from multiple sources in one request
    using curly brace notation, in example:
        'my_server.{my_instance1,my_instance2}.cpu'
    This class defines interface for building that value list

    Example:
        >>> values = GraphiteMultipleValue('foo', bar', 'spam')
        >>> str(values)
        >>> '{foo,bar,spam}'
    """

    def __init__(self, *values: str) -> None:
        self.values = values

    def __str__(self) -> str:
        """
        Converts each value to string and joins them with comma symbol

        :returns: string of comma-separated values wrapped in curly braces
        """
        return f'{{{",".join(map(str, self.values))}}}'
